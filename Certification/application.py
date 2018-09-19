#coding: utf-8

from school import School, hash128
from stellar_base.keypair import Keypair
from stellar_base.horizon import Horizon
from hashlib import sha256
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
            response = school.award_degree(request.form['address'], name, request.form['birthdate'], request.form['year'])
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1, txhash=response['hash'])
        except Exception as e:
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   school=1, awarderror=e)

    @webapp.route('/check_degree', methods=['GET', 'POST'])
    def check_degree():
        if request.method == 'GET':
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   verif=1)
        horizon = Horizon()
        try:
            if request.args.get('txhash') is defined:
                tx = horizon.transaction(request.args.get('txhash'))
            elif request.args.get('txqr') is defined:
                pass
            else:
                raise Exception("Vous devez spécifier au moins un hash OU un qrcode")
            # Hashing infos from the from to check the hash with the one in the transaction's memo
            name = request.args.get('name')
            birthdate = request.args.get('birthdate')
            year = request.args.get('year')
            h = hash128((name+birthdate+year).encode())
            if h == tx.get('memo'):
                return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   verif=1, verif_passed=1, id=tx.get('source_account'),
                                   name=name, birthdate=birthdate, year=year)
            else:
                return render_template('index.html', js_folder=url_for('static', filename='js'),
                                       img_folder=url_for('static', filename='img'),
                                       css_folder=url_for('static', filename='css'),
                                       verif=1, veriferror="Les informations saisies ne correspondent pas avec l'exemplaire du diplôme décerné")
        except Exception as e:
            try:
                tx = Horizon.transaction(request.args.get('txqr'))
            except Exception as e:
                return render_template('index.html', js_folder=url_for('static', filename='js'),
                                       img_folder=url_for('static', filename='img'),
                                       css_folder=url_for('static', filename='css'),
                                       verif=1, veriferror=e)

    def run(self, host, port):
        webapp.run(host, port, debug=True)

if __name__ == '__main__':
    app = App()
    app.run('0.0.0.0', '5010')
