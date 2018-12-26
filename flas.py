import request  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import os.path
from flask import Flask, render_template, redirect, url_for, request
import jangteor_bs4

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('mainpage.html')


@app.route('/search_button.png')
def buttonImg():
    return redirect(url_for('static', filename='searchbutton.png'))

@app.route('/search_page', methods=['POST'])
def search():
    print('search')
    value = request.form['item']
    jangteor_bs4.get_info2(value)
    return render_template('searchpage.html')


# search page -> iframe -> csv

@app.route('/iframe_auction.html')
def iframeau():
    return render_template('iframeauction.html')


@app.route('/jangteor_crawling2.csv')
def jangteor():
    return redirect(url_for('static', filename='jangteor_crawling2.csv'))



if __name__ == '__main__':
    app.run(debug=True)
