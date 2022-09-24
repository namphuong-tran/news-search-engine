#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
from error import errorultils
from crawler.newschannels import NewsChannels
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


def connect_database():
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    # Read mysql config file
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    # Create insert query
    mysql = MySql(cfg_dic, 'mysql')
    return mysql


def crawl_articles(url_list, channel, selected_date = None):
    mysql = connect_database()
    insert_sql = mysql.create_insert_sql('es_table', 'REPLACE', 10)
    if(selected_date != None):
        exist_articles = get_exist_articles_by_channel(
            mysql, channel, selected_date)
        url_list = list(set(url_list) - set(exist_articles))
    print(len(url_list))
    error_url = []
    for url in url_list:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            authors = ', '.join(article.authors)
            publish_date = article.publish_date.strftime('%Y-%m-%d')
            keywords = ', '.join(article.keywords)
            summary = article.summary
            text = article.text
            modification_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            news = [uuid.uuid4(), title, channel, authors,
                    publish_date, keywords, summary, text, url, modification_time]
            mysql.execute(insert_sql, news)
        except Exception:
            error_url.append(url)
            logging.error(url)
            logging.exception("Crawler exception was thrown!")
    print(len(error_url))
    errorultils.write_error_url(error_url, channel)


def get_exist_articles_by_channel(mysql, channel, selected_date):

    if (channel == NewsChannels.NBC.value):
        # get all articles in this month
        selected_date = datetime.strptime(
            selected_date, '%Y-%m-%d').replace(day=1).strftime("%Y-%m-%d")
        conditions = [mysql.MySqlCondition('newspaper', MySql.MySqlCondition.EQUAL),
                      mysql.MySqlCondition('publish_date', MySql.MySqlCondition.GREATER)]
    else:
        # get only articles published in selected date
        conditions = [mysql.MySqlCondition('newspaper', MySql.MySqlCondition.EQUAL),
                      mysql.MySqlCondition('publish_date', MySql.MySqlCondition.EQUAL)]

    query_sql = mysql.create_query_sql(
        'es_table', ['url'], conditions)
    params = (channel, selected_date)
    mysql.execute(query_sql, params)
    result = [item for t in list(mysql.cur.fetchall()) for item in t]
    return result


if __name__ == '__main__':
    channel = sys.argv[1]
    crawl_articles(url_list=errorultils.read_error_url(channel), channel=channel, selected_date=None)
