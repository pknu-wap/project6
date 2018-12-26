import request  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import os.path
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('mainpage.html')
@app.route('/searchbutton.png')
def buttonImg():
    return redirect(url_for('static', filename='searchbutton.png'))

@app.route('/iframeauction')
def iframeau():
    return render_template('iframeauction.html')


@app.route('/search', methods=['POST'])
def search():
    print('a')
    value = request.form['item']
    return value



if __name__ == '__main__':

    app.run(debug=True)
