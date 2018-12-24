#물건 링크가 옥션, 경매 등 다양하게 있어서
#이 소스코드에서는 최종수정일만 링크가 중고장터인 것만 뽑음
#selenium, BeautifulSoip, Wendriver 필요
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def get_info(item):
    res_lis = []
    if(f_name == '0'):
        path = f_path
    else:
        path = '/Users/' + f_name + '/Downloads/chromedriver'
    if(brow == 1):
        driver = webdriver.Chrome(path)
    if(brow == 2):
        driver = webdriver.Firefox(path)
    if(brow == 3):
        driver = webdriver.Edge(path)
    if(brow == 4):
        driver = webdriver.Opera(path)
    if(brow == 5):
        driver = webdriver.Safari(path)
    
    item = item.encode('unicode_escape')
    item = str(item)[2:-1].replace('\\\\', '%')
    
    driver.get('http://corners.auction.co.kr/corner/UsedMarketList.aspx' + '?keyword=' + item)
    html = driver.page_source
    try: #'더 보기'가 있다면 모든 '더 보기' 클릭
        bsobj = BeautifulSoup(html, 'html.parser')
        page = bsobj.find('div', {'class':'page'}).text
        page_number = page.split('/')
        page_max = page_number[1]
        for i in range(1, int(page_max)):
            time.sleep(1)
            driver.find_element_by_css_selector('#ucPager_dListMoreView > a').click()
    except:
        pass
    html = driver.page_source
    bsobj = BeautifulSoup(html, 'html.parser')
    divs = bsobj.find_all('div', {'class':'list_view'})
    for div in divs: #제목, 가격, 배송비, url 뽑기
        div_item = div.find('div', {'class':'item_title type1'})
        title = div_item.find('a').text
        url_item = div_item.find('a')['href']
        span = div.find('span', {'class':'now'})
        price = span.find('strong').text
        try:
            del_fee = div.find('div', {'class':'icon ic_delivery'}).text
        except:
            del_fee = '무료 배송'
        a_link = div.find('a')['href']
        num_of_pagedowns = 5
        driver.get(a_link)
        body = driver.find_element_by_tag_name('body')
        while num_of_pagedowns: #스크롤이 내려간 이벤트 후, 정보가 불러와지기 때문에 스크롤을 내림
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
            num_of_pagedowns -= 1
        html = driver.page_source
        bsobj = BeautifulSoup(html, 'html.parser')
        try:
            div_date = bsobj.find('div', {'class':'seller_update'})
            date = div_date.find('span', {'id':'spanNewDescriptionLastUpdate'}).text
        except:
            date = 'NONE'
        res_lis.append({'title':title, 'price':price, 'delivery fee':del_fee, 'url':url_item, 'date':date})    
    jangteor = pd.DataFrame(res_lis)
    jangteor.to_csv('jangteor_crawling.csv', mode='w', index=False)

print('옥션 중고장터 크롤러입니다.')
item = input('검색할 물품을 입력하세요: ')
brow = int(input('사용할 브라우저를 입력해주세요(1. Chrome, 2.Firefox, 3.Edge, 4.Opera, 5.Safari): '))
f_name = input('사용자 파일명을 입력해주세요(웹드라이버의 경로가 바뀌었다면 0을 입력해주세요): ')
f_path = ''
if(f_name == '0'):
    f_path = input('경로를 입력해주세요: ')
    
get_info(item)
