#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import datetime
import crawler
import channel_name


class USATodayCrawler:

    def __init__(self, selected_date):
        self.selected_date = selected_date

    def get_link_articles(self):
        aritcle_url_list = []
        page_url_list = []
        targeted_url = self.generate_targeted_url(self.selected_date)
        html = requests.get(targeted_url)
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')
        pagination = sp.find(
            'ul', {'class': 'sitemap-list sitemap-pagination'})

        for page in pagination.find_all('li', {'class': 'sitemap-list-item'}):
            page_url_list.append(page.find('a').get('href'))

        # get article url in page 1
        aritcle_url_list.extend(self.get_link_article_pagination(None, sp))
        # get article url from page 2
        for i in range(1, len(page_url_list)):
            aritcle_url_list.extend(self.get_link_article_pagination(
                page_url_list[i], None))

        return aritcle_url_list

    def get_link_article_pagination(self, page_url=None, soup=None):
        artile_url_list = []
        if (soup == None):
            html = requests.get(page_url)
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
        main_content = soup.find('div', {'class': 'sitemap-column-wrapper'})
        article_list = main_content.find('ul', {'class': 'sitemap-list'})
        for article_element in article_list.find_all('li'):
            artile_url_list.append(article_element.find('a').get('href'))

        return artile_url_list

    @staticmethod
    def generate_targeted_url(selected_date, page=None):
        year = selected_date.split('-')[0]
        month_num = selected_date.split('-')[1]
        # Mapping month number to full month name in lowercase(Eg: 09 -> september)
        month_name = datetime.datetime(1, int(month_num), 1).strftime("%B")
        # Convert number in string to short style (Eg: 01 to 1)
        day = int(selected_date.split('-')[2])
        if (page == None):
            page = 1
        return "https://www.usatoday.com/sitemap/{}/{}/{}/?page={}".format(year, month_name, day, page)


if __name__ == '__main__':
    selected_date = sys.argv[1]
    usa_today_crawler = USATodayCrawler(selected_date)
    url_list = usa_today_crawler.get_link_articles()
    print(len(url_list))

    crawler.crawl_articles(url_list, channel_name.USATODAY)
