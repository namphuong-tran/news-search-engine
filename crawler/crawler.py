import channel_name
import logging
from datetime import datetime
from select import select
import sys
# sys.path.append('/home/namphuong/Code/news-search-engine/news-search-engine/')
# sys.path.insert(0, '/home/namphuong/Code/news-search-engine/news-search-engine/')
# export PYTHONPATH='/home/namphuong/Code/news-search-engine/news-search-engine/'
from mysqlclient.inserting import ReadConfig, MySql
import uuid
from newspaper import Article
import nltk
nltk.download('punkt')


def crawl_articles(url_list, channel, selected_date):
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    # Read mysql config file
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    # Create insert query
    mysql = MySql(cfg_dic, 'mysql')
    user_sql = mysql.create_insert_sql('es_table', 'REPLACE', 10)
    exist_articles = get_exist_articles_by_channel(
        mysql, channel, selected_date)
    url_list = list(set(url_list) - set(exist_articles))
    print(len(url_list))
    for url in url_list:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            authors = ', '.join(article.authors)
            publish_date = article.publish_date
            keywords = ', '.join(article.keywords)
            summary = article.summary
            text = article.text
            modification_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            news = [uuid.uuid4(), title, channel, authors,
                    publish_date, keywords, summary, text, url, modification_time]
            mysql.execute(user_sql, news)
        except Exception:
            logging.error(url)
            logging.exception("Crawler exception was thrown!")


def get_exist_articles_by_channel(mysql, channel, selected_date):

    if (channel == channel_name.NBC):
        # get all articles in this month
        selected_date = datetime.strptime(
            selected_date, '%Y-%m-%d').replace(day=1).strftime("%Y-%m-%d")
        conditions = [mysql.MySqlCondition('newspaper', MySql.MySqlCondition.EQUAL),
                      mysql.MySqlCondition('publish_date', MySql.MySqlCondition.GREATER)]
    else:
        # get only articles published in selected date
        conditions = [mysql.MySqlCondition('newspaper', MySql.MySqlCondition.EQUAL),
                      mysql.MySqlCondition('publish_date', MySql.MySqlCondition.EQUAL)]

    sql_query = mysql.create_query_sql(
        'es_table', ['url'], conditions)
    params = (channel, selected_date)
    mysql.execute(sql_query, params)
    result = [item for t in list(mysql.cur.fetchall()) for item in t]
    return result
