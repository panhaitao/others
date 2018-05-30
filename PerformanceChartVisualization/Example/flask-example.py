from flask import Flask, url_for
import os
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/run/<command>')
def api_articles(command):
    return os.popen(command).read()

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run(host='0.0.0.0')
