import requests
from bs4 import BeautifulSoup
import xlwt
from urllib.parse import urljoin


class Junggonara:
    def __init__(self, query, end_page, worksheet):
        self.query = query
        self.worksheet = worksheet
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

    def paste_to_csv(self, i, idx, number, select_list):
        try:
            tag = select_list[0]
            self.worksheet.write(20 * i + idx, number, tag.text)
        except IndexError:
            self.worksheet.write(20 * i + idx, number, 'None')

    def paste_title(self, i, iterable):
        idx = 1
        for tag in iterable:
            self.worksheet.write(20 * i + idx, 0, tag.text)
            idx += 1

    def crawling(self):
        res_lis = []
        for i in range(self.end_page):
            params = self.get_params()
            params['search.page'] = i + 1
            html = requests.get(list_url, headers=headers, params=params).text
            soup = BeautifulSoup(html, 'html.parser')
            self.paste_title(i, soup.select('li .item h3'))

            idx = 1
            for tag in soup.select('.list_tit li > a'):
                link_url = tag['href']
                article_url = urljoin(list_url, link_url)
                html2 = requests.get(article_url, headers=headers).text
                soup2 = BeautifulSoup(html2, 'html.parser')
                self.paste_to_csv(i, idx, 1, soup2.select('.price'))
                self.paste_to_csv(i, idx, 2, soup2.select('.board_time span'))
                #self.worksheet.write(20 * i + idx, 3, article_url)
                self.worksheet.write(20 * i + idx, 3, article_url)
                idx += 1
                    del_fee = '무료 배송'
                res_lis.append({'price' : soup2.select('.price'), 'span' : soup2.select('.board_time span')})
        Junggonara = pd.DataFrame(res_lis)
        Junggonara.to_csv('tjunggo.csv', mode='w', index=False)


list_url = 'https://m.cafe.naver.com/ArticleSearchList.nhn'
headers = {
    'Referer': 'https://m.cafe.naver.com/joonggonara',
}
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('중고나라')
worksheet.write(0, 0, '글 제목')
worksheet.write(0, 1, '가격')
worksheet.write(0, 2, '올린 시간')
worksheet.write(0, 3, 'url')


search_item = input("구매하려는 물건을 입력하시오 : ")
find_item = Junggonara(search_item, 10, worksheet)
find_item.crawling()
workbook.save('junggo.csv')
