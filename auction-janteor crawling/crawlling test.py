#!/usr/bin/env python
# coding: utf-8

# ## 파이썬 크롤링 ( 중고나라 크롤링(갑자기 오류..), 중고장터 크롤링)

# In[50]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def get_info(ids, pws, que):#captcha가 뜰 경우 30초안에 입력해주세요
    page = '1'
    driver = webdriver.Chrome('/Users/wonseok/Downloads/chromedriver')
    driver.get('http://naver.com/')
    driver.find_element_by_css_selector('#account > div > a > i').click()
    for id in ids:
        driver.find_element_by_name('id').send_keys(id)
    for pw in pws:
        driver.find_element_by_name('pw').send_keys(pw)
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
    time.sleep(30)
    
    while(page[0:1]):
        base_url = 'https://cafe.naver.com/joonggonara?iframe_url=/joongonara/ArticleList.nhn%3Fsearch.clubid=10050146'
        addurl = '&search.menuid==***&search.page==%d' + page
        driver.get(base_url + addurl)
        driver.switch_to.frame('cafe_main')
        driver.find_element_by_name('query').send_keys(que)
        driver.find_element_by_css_selector("#main-area > div.list-search > form > div.input_search_area > button").click()
        article_list = driver.find_elements_by_css_selector('div.inner_list > a.article')
        article_urls = [ i.get_attribute('href') for i in article_list]
        
        for article in article_urls:
            try:
                driver.get(article)
                driver.switch_to.frame('cafe_main')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                title = soup.select('div.tit-box span.b')[0].get_text()
                price = soup.select('div.prod_price span.cost')[0].get_text()
                day = soup.select('div.tit-box div.fr td.m-tcol-c')[0].get_text()
                res_list.append({'title':title, 'price':price, 'day':day, 'url':article})
            except:
                print('잠시만 기다려 주세요')
        joongo = pd.DataFrame(res_list)
        joongo.to_csv('joongonara_crawling.csv', mode='w', index=False)
        page = input("더 찾아볼 페이지를 입력하세요(종료는 0): ")

        
url = []
ids = input("네이버 아이디를 입력해주세요: ")
pws = input("비밀번호를 입력해주세요: ")
que = input("찾아볼 물건을 입력하세요: ")
get_info(ids, pws, que)



# In[46]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def get_info(item):
    res_lis = []
    driver = webdriver.Chrome('/Users/wonseok/Downloads/chromedriver')
    driver.get('http://corners.auction.co.kr/corner/UsedMarketList.aspx' + '?keyword=' + item)
    html = driver.page_source
    bsobj = BeautifulSoup(html, 'html.parser')
    page = bsobj.find('div', {'class':'page'}).text
    page_number = page.split('/')
    page_max = page_number[1]
    for i in range(1, int(page_max)):
        time.sleep(1)
        driver.find_element_by_css_selector('#ucPager_dListMoreView > a').click()
        html = driver.page_source
        bsobj = BeautifulSoup(html, 'html.parser')
        divs = bsobj.find_all('div', {'class':'list_view'})
        for div in divs:
            div_item = div.find('div', {'class':'item_title type1'})
            title = div_item.find('a').text
            url_item = div_item.find('a')['href']
            span = div.find('span', {'class':'now'})
            price = span.find('strong').text
            if(div.find('div', {'class':'icon ic_delivery'})):
                del_fee = div.find('div', {'class':'icon ic_delivery'}).text
            else:
                del_fee = '무료 배송'
            res_lis.append({'title':title, 'price':price, 'delivery fee':del_fee, 'url':url_item})
    jangteor = pd.DataFrame(res_lis)
    jangteor.to_csv('jangteor_crawling.csv', mode='w', index=False)

item = input('검색할 물품를 입력하세요: ')
get_info(item)


# In[ ]:




