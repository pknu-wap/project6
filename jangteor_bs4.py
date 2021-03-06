#최종정보수정일은 Beautifulsoup 라이브러리 만으로 구하기 힘듦 -> 삭제
#BeautifulSoip필요
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

def get_info2(item):
    print('debug')
    res_lis = []
    page = 0
    url = 'http://corners.auction.co.kr/corner/UsedMarketList.aspx?keyword=' + item
    html = requests.get(url).text
    bsobj = BeautifulSoup(html, 'html.parser')
    try:
        max_page = bsobj.find('div', {'class':'page'}).text
        max_page_number = max_page.split('/')
        max_page_max = max_page_number[1]
    except:
        max_page_max = 1
    
    for ind in range(0,int(max_page_max)):
        url = 'http://corners.auction.co.kr/corner/UsedMarketList.aspx?keyword=' + item +'&page=' + '{0}'.format(page)
        html = requests.get(url).text
        bsobj = BeautifulSoup(html, 'html.parser')
        divs = bsobj.find_all('div', {'class':'list_view'})
        print(len(divs))
        for div in divs: #제목, 가격, 배송비, url 뽑기
            div_item = div.find('div', {'class':'item_title type1'})
            title = div_item.find('a').text.replace(',','')
            url_item = div_item.find('a')['href']
            span = div.find('span', {'class':'now'})
            price = span.find('strong').text.replace(',','')
            try:
                del_fee = div.find('div', {'class':'icon ic_delivery'}).text.replace(',','')
            except:
                del_fee = '무료 배송'
            res_lis.append({'title':title, 'price':price, 'delivery fee':del_fee, 'url':url_item})

    jangteor = pd.DataFrame(res_lis)
    jangteor.to_csv('static/jangteor_crawling2.csv', mode='w', index=False)

#if __name__ == '__main__':
#    get_info2(sys.argv[1])
