import request  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import os.path
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('mainpage.html')


@app.route('/search_button.png')
def buttonImg():
    return redirect(url_for('static', filename='searchbutton.png'))


@app.route('/search_page', methods=['POST'])
def search():
    value = request.form['item']
    # val_검색결과
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
