#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from time import strptime
import channel_name
import crawler


class ReutersCrawler:
    ROOT_URL = 'https://www.reuters.com'

    def __init__(self, selected_date):
        self.selected_date = selected_date
        self.is_next_page = True
        self.num_page = 0

    def get_link_articles(self):
        aritcle_url_list = []

        while (self.is_next_page):
            aritcle_url_list.extend(self.get_link_article_pagination())

        return aritcle_url_list

    def get_link_article_pagination(self):
        artile_url_list = []
        self.num_page = self.num_page + 1
        targeted_url = self.generate_targeted_url(self.num_page)
        html = requests.get(targeted_url)
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')
        main_content = sp.find('div', {'class': 'news-headline-list'})
        current_date = date.today()
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        for article_element in main_content.find_all('article', {'class': 'story'}):
            # Convert publish date to format '%Y-%m-%d' (Eg. 2022-09-01)
            publish_date = article_element.find(
                'span', {'class': 'timestamp'}).get_text()
            if ('EDT' in publish_date.split()):
                publish_date = current_date
            else:
                year = publish_date.split()[2]
                day = publish_date.split()[1]
                month = strptime(publish_date.split()[0], '%b').tm_mon
                # convert a single digit number into a double digits string (Eg 9 => 09)
                month = f'{month:02d}'
                publish_date = year + '-' + month + '-' + day
                publish_date = datetime.strptime(
                    publish_date, '%Y-%m-%d').date()

            # Compare publish date with selected date in order to collect articles
            if (selected_date_obj == publish_date):
                artile_url_list.append(
                    self.ROOT_URL + article_element.find('a').get('href'))
            if (publish_date < selected_date_obj):
                self.is_next_page = False

        return artile_url_list

    @staticmethod
    def generate_targeted_url(page):
        return "https://www.reuters.com/news/archive?view=page&page={}&pageSize=10".format(page)


if __name__ == '__main__':
    selected_date = sys.argv[1]
    reuters_crawler = ReutersCrawler(selected_date)
    url_list = reuters_crawler.get_link_articles()
    print(len(url_list))
    crawler.crawl_articles(url_list, channel_name.REUTERS)
