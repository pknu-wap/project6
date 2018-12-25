import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Junggonara:
    def __init__(self, query, end_page):
        self.query = query
        self.end_page = end_page

    def get_params(self):
        params = {
            'search.query': self.query,
            'search.menuid': None,
            'search.searchBy': 1,
            'search.sortBy': 'date',
            'search.clubid': 10050146,
            'search.option': 0,
            'search.defaultValue': None,
        }
        return params

    def paste_to_csv(self, title, price, span, res_list):
        try:
            res_list.append({'title':title.text.split(':')[0], 'price':price[0].text, 'date':span[0].text})
        except:
            pass

    def crawling(self):
        res_list = []
        for i in range(self.end_page):
            params = self.get_params()
            params['search.page'] = i + 1
            html = requests.get(list_url, headers=headers, params=params).text
            soup = BeautifulSoup(html, 'html.parser')

            for tag in soup.select('.list_tit li > a'):
                link_url = tag['href']
                article_url = urljoin(list_url, link_url)
                html2 = requests.get(article_url, headers=headers).text
                soup2 = BeautifulSoup(html2, 'html.parser')
                self.paste_to_csv(soup2.find('title'), soup2.select('.price'), soup2.select('.board_time span'), res_list)
        joonggo = pd.DataFrame(res_list)
        joonggo.to_csv('joonggonara.csv', mode='w', index=False)


list_url = 'https://m.cafe.naver.com/ArticleSearchList.nhn'
headers = {
    'Referer': 'https://m.cafe.naver.com/joonggonara',
}

def crawl_start():
    search_item = input("구매하려는 물건을 입력하시오 : ")
    find_item = Junggonara(search_item, 10)
    find_item.crawling()

