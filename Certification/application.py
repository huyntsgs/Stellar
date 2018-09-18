#coding: utf-8

from school import School
from stellar_base.keypair import Keypair
from flask_qrcode import QRcode
from flask import Flask, render_template, url_for, request, session
webapp = Flask(__name__)
QRcode(webapp)

class App:
    def __init__(self):
        webapp.secret_key = b'Z\xf4{\xe1\xfd\x18\x03(\xb0\xb6\xc8\xf0@\x0e\xf5\xffR\xf4\x1eM\xb2\x8b`\x95T\xb9g\xff\xf2rZS'

    @webapp.route('/index.html')
    @webapp.route('/index')
    @webapp.route('/')
    def index():
        session.clear()# For dev
        return render_template('index.html', js_folder=url_for('static', filename='js'),
                               img_folder=url_for('static', filename='img'),
                               css_folder=url_for('static', filename='css'))

    @webapp.route('/school_login', methods=['POST', 'GET'])
    def school_login():
        # To be able to reload
        if request.method == 'GET':
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1)
        try:
            Keypair.from_seed(request.form['secret']) # To check if the key is valid
            session['school_seed'] = request.form['secret']
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1)
        except:
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1, formschoolerror=1)
    @webapp.route('/award_degree', methods=['POST', 'GET'])
    def award_degree():
        # To be able to reload
        if request.method == 'GET':
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1)
        try:
            school = School(session['school_seed'])
            name = request.form['name'].lower()
            response = school.award_degree(request.form['address'], request.form['token_name'], name, request.form['year'])
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1, txhash=response['hash'])
        except Exception as e:
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1, awarderror=e)


    def run(self, host, port):
        webapp.run(host, port)

if __name__ == '__main__':
    app = App()
    app.run('0.0.0.0', '5010')
