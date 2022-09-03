import pandas as pd
from datetime import datetime
import mysql.connector as mysql
from newspaper import Newspaper
#!/home/namphuong/Code/news-search-engine/myvenv/bin/python

import sys


class Database:
    def __init__(self, host, user, pwd, database):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.database = database

    def get_connection(self):
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.pwd,
            database=self.database
        )
        return connection

    @staticmethod
    def insert_data(connection, cursor, news):
        query = "INSERT INTO es_table (id, title, newspaper, authors, publish_date, keywords, summary, text, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (news.id, news.title, news.newspaper,
                  news.authors, news.publish_date, news.keywords,
                  news.summary, news.text, news.url)
        cursor.execute(query, values)
        connection.commit()
        


if __name__ == '__main__':
    db = Database('localhost', 'system', 'admin123', 'temp_db')
    connection = db.get_connection()
    cursor = connection.cursor()
    # file_name = '/home/namphuong/Downloads/cnn_2021_test.csv'
    file_name = sys.argv[1]

    df = pd.read_csv(file_name)
    df = df.reset_index()
    for index, row in df.iterrows():
        publish_date = datetime.strptime(row['publish_date'], '%Y-%m-%d')
        news = Newspaper(row['id'], row['title'], row['newspaper'],
                         row['authors'], publish_date, row['keywords'],
                         row['summary'], row['text'], row['url'])
        db.insert_data(connection, cursor, news)
        print(index, "record inserted")

