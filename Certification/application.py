#coding: utf-8

from flask import Flask, render_template, url_for, request
webapp = Flask(__name__)

class App:
    def __init__(self):
        pass

    @webapp.route('/index.html', methods=['GET'])
    @webapp.route('/index', methods=['GET'])
    @webapp.route('/', methods=['GET'])
    def index():
        return render_template('index.html', js_folder=url_for('static', filename='js'), img_folder=url_for('static', filename='img'), css_folder=url_for('static', filename='css'))

    @webapp.route('/school_login', methods=['POST'])
    def school_login():
        school_seed = request.form['secret']
        return render_template('index.html', js_folder=url_for('static', filename='js'), img_folder=url_for('static', filename='img'), css_folder=url_for('static', filename='css'), school=1)
    
    def run(self, host):
        webapp.run(host)

if __name__ == '__main__':
    app = App()
    app.run(host='0.0.0.0')
