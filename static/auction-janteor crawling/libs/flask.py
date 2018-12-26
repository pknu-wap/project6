Skip
to
content

Search or jump
to…

Pull
requests
Issues
Marketplace
Explore


@Awseok


Sign
out
0
0
0
pknu - wap / project6
Code
Issues
0
Pull
requests
0
Projects
0
Wiki
Insights
project6 / 연동 / flask_server.py
2850736
6
hours
ago


@hyesung


-comet
hyesung - comet
interlock
main_page.html
with flask_server.py

61
lines(52
sloc)  1.97
KB
from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

item = ""


@app.route('/')
@app.route('/<string:item>')
def flaskServer(item=None):
    return render_template('main_page.html', item=item)


@app.route('/search', methods=['POST'])
def search(item=None):
    if request.method == 'POST':
        temp = request.form['item']
    else:
        temp = None
    return redirect(url_for('get_info', item=temp))


@app.route('/')
@app.route('/<string:item>')
def get_info(item):
    res_lis = []
    page = 0
    url = 'http://corners.auction.co.kr/corner/UsedMarketList.aspx?keyword=' + item
    html = requests.get(url).text
    bsobj = BeautifulSoup(html, 'html.parser')
    try:
        max_page = bsobj.find('div', {'class': 'page'}).text
        max_page_number = max_page.split('/')
        max_page_max = max_page_number[1]
    except:
        max_page_max = 1

    for ind in range(0, max_page_max):
        url = 'http://corners.auction.co.kr/corner/UsedMarketList.aspx?keyword=' + item + '&page=' + '{0}'.format(page)
        html = requests.get(url).text
        bsobj = BeautifulSoup(html, 'html.parser')
        divs = bsobj.find_all('div', {'class': 'list_view'})

        for div in divs:  # 제목, 가격, 배송비, url 뽑기
            div_item = div.find('div', {'class': 'item_title type1'})
            title = div_item.find('a').text
            url_item = div_item.find('a')['href']
            span = div.find('span', {'class': 'now'})
            price = span.find('strong').text
            try:
                del_fee = div.find('div', {'class': 'icon ic_delivery'}).text
            except:
                del_fee = '무료 배송'
            res_lis.append({'title': title, 'price': price, 'delivery fee': del_fee, 'url': url_item})
    jangteor = pd.DataFrame(res_lis)
    jangteor.to_csv('jangteor_crawling2.csv', mode='w', index=False)


get_info(item)

if __name__ == '__main__':
    app.run()
© 2018
GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact
GitHub
Pricing
API
Training
Blog
About
Press
h
to
open
a
hovercard
with more details.