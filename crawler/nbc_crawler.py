#!/home/namphuong/Code/news-search-engine/myvenv/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import datetime


class NBCCrawler:

    def __init__(self, selected_date):
        self.selected_date = selected_date

    def get_link_articles(self):
        aritcle_url_list = []
        page_url_list = []
        targeted_url = self.generate_targeted_url(self.selected_date)
        html = requests.get(targeted_url)
        html.encoding = 'utf-8'
        sp = BeautifulSoup(html.text, 'lxml')
        
        # get article url in page 1
        aritcle_url_list.extend(self.get_link_article_pagination(None, sp))

        pagination = sp.find(
            'div', {'class': 'Pagination__numbers'})
        if (pagination != None):
            for page in pagination.find_all('a', {'class': 'Pagination__num'}):
                page_url_list.append(page.get('href'))

            # get article url from page 2
            for i in range(0, len(page_url_list)):
                page_url = self.generate_targeted_url(self.selected_date, i+2)
                aritcle_url_list.extend(
                    self.get_link_article_pagination(page_url, None))

        return aritcle_url_list

    def get_link_article_pagination(self, page_url=None, soup=None):
        artile_url_list = []
        if (soup == None):
            html = requests.get(page_url)
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
        main_content = soup.find('main', {'class': 'MonthPage'})
        for article_element in main_content.find_all('a'):
            artile_url_list.append(article_element.get('href'))

        return artile_url_list

    @staticmethod
    def generate_targeted_url(selected_date, page=None):
        year = selected_date.split('-')[0]
        month_num = selected_date.split('-')[1]
        # Mapping month number to full month name in lowercase(Eg: 09 -> september)
        month_name = datetime.datetime(
            1, int(month_num), 1).strftime("%B").lower()
        # Convert number in string to short style (Eg: 01 to 1)
        day = int(selected_date.split('-')[2])
        if (page == None):
            page = ''
        return "https://www.nbcnews.com/archive/articles/{}/{}/{}".format(year, month_name, page)


if __name__ == '__main__':
    selected_date = sys.argv[1]
    crawler = NBCCrawler(selected_date)
    url_list = crawler.get_link_articles()
    print(len(url_list))
