#coding: utf-8

from flask import Flask, render_template, url_for
webapp = Flask(__name__)

class App:
    def __init__(self):
        pass

    @webapp.route('/index.html')
    @webapp.route('/index')
    @webapp.route('/')
    def index():
        return render_template('index.html', js_folder=url_for('static', filename='js'), img_folder=url_for('static', filename='img'), css_folder=url_for('static', filename='css'))

    def run(self, host):
        webapp.run(host)

if __name__ == '__main__':
    app = App()
    app.run(host='0.0.0.0')
