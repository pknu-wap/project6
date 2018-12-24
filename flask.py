import requests # pip install requests 
from bs4 import BeautifulSoup # pip install bs4

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    req = requests.get('')
    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok

    if is_ok: 
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('#contents > ul > li > a')
        return render_template('main.html', titles = title)
    else:
        return '가져오기 실패'

if __name__=='__main__':
    app.run()