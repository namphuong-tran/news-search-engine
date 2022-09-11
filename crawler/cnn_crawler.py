#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import channel_name
import crawler


class CNNCrawler:

    def __init__(self, selected_date):
        self.selected_date = selected_date

    def get_link_articles(self):
        url_list = []
        selected_year = self.selected_date.split('-')[0]
        selected_month = self.selected_date.split('-')[1]
        selected_day = self.selected_date.split('-')[2]
        targeted_url = self.generate_targeted_url(
            selected_year, selected_month)
        html = requests.get(targeted_url)
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')
        article_list = sp.findAll('div', {'class': 'sitemap-entry'})[1]

        for article_element in article_list.find_all('li'):
            article = article_element.find_all('span')
            publish_date = article[0].get_text().split('-')[2]

            if (publish_date == selected_day):
                link = article[1].find('a').get('href')
                url_list.append(link)

        return url_list

    @staticmethod
    def generate_targeted_url(year, month):
        return "https://edition.cnn.com/article/sitemap-{}-{}.html".format(year, month)


if __name__ == '__main__':
    selected_date = sys.argv[1]
    cnn_crawler = CNNCrawler(selected_date)
    url_list = cnn_crawler.get_link_articles()
    print(len(url_list))
    crawler.crawl_articles(url_list, channel_name.CNN)
