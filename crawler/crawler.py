from datetime import datetime
import sys
# sys.path.append('/home/namphuong/Code/news-search-engine/news-search-engine/')
# sys.path.insert(0, '/home/namphuong/Code/news-search-engine/news-search-engine/')
# export PYTHONPATH='/home/namphuong/Code/news-search-engine/news-search-engine/'
from mysqlclient.inserting import ReadConfig, MySql
import uuid
from newspaper import Article
import nltk
nltk.download('punkt')
import logging

def crawl_articles(url_list, chanel_name):
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    print(cfg_dic)
    # Read mysql config file
    cfg = ReadConfig()
    cfg_dic = cfg.get_config()
    # Create insert query
    mysql = MySql(cfg_dic, 'mysql')
    user_sql = mysql.create_insert_sql('es_table', 'REPLACE', 10)
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
            news = [uuid.uuid4(), title, chanel_name, authors,
                    publish_date, keywords, summary, text, url, modification_time]
            mysql.execute(user_sql, news)
        except Exception:
            logging.exception("Crawler exception was thrown!")
            logging.info(url)