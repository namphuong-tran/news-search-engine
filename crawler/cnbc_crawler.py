#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
import logging
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import crawlers
from crawler.newschannels import NewsChannels


class CNBCCrawler:

    def __init__(self, selected_date):
        self.selected_date = selected_date

    def get_link_articles(self):
        url_list = []
        targeted_url = self.generate_targeted_url(self.selected_date)
        html = requests.get(targeted_url)
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')
        for article_element in sp.find_all('a', {'class': 'SiteMapArticleList-link'}):
            url_list.append(article_element.get('href'))

        return url_list

    @staticmethod
    def generate_targeted_url(selected_date):
        year = selected_date.split('-')[0]
        month_num = selected_date.split('-')[1]
        # Mapping month number to full month name (Eg: 09 -> September)
        month_name = datetime(1, int(month_num), 1).strftime("%B")
        # Convert number in string to short style (Eg: 01 to 1)
        day = int(selected_date.split('-')[2])
        return "https://www.cnbc.com/site-map/articles/{}/{}/{}/".format(year, month_name, day)


if __name__ == '__main__':
    selected_date = sys.argv[1]
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    if (selected_date_obj <= datetime.today()):
        cnbc_crawler = CNBCCrawler(selected_date)
        url_list = cnbc_crawler.get_link_articles()
        print(len(url_list))
        crawlers.crawl_articles(
            url_list, NewsChannels.CBNC.value, selected_date)
    else:
        logging.error("Selected date is invalid")
