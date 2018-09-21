#coding: utf-8

from school import School, hash128
from stellar_base.keypair import Keypair
from stellar_base.horizon import Horizon

from werkzeug.utils import secure_filename
import qreader
import os

from flask_qrcode import QRcode
from flask import Flask, render_template, url_for, request, session
webapp = Flask(__name__)
QRcode(webapp)

class App:
    """
    The class used to wrap up the whole web application.
    """
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
            # In this part we try to get the hash of the transaction in order to fetch it from horizon. The hash is easier to get from text,
            # that's why it's the first test.
            if 'txhash' in request.form and request.form.get('txhash'):
                tx = horizon.transaction(request.form.get('txhash'))
            elif 'txqr' in request.files:
                # If a qrcode is submitted, we have to save it to decode it, which causes security issues.
                qr = request.files.get('txqr')
                # if user does not select file, browser also
                # submit an empty part without filename
                if qr.filename == '':
                    raise Exception("Vous devez spécifier au moins un hash OU un qrcode")
                else:
                    if app.allowed_filename(qr.filename):
                        fname = secure_filename(qr.filename)
                        fpath = os.path.join(os.getcwd(), 'static', fname)
                        qr.save(fpath)
                        data = qreader.read(fpath)
                        os.remove(fpath) # We don't need it anymore
                        tx = horizon.transaction(data)
                    else:
                        raise Exception("Merci de ne passer que des images générées par ce site")
            else:
                raise Exception("Vous devez spécifier au moins un hash OU un qrcode")

            # Hashing infos from the form to check the hash with the one in the transaction's memo
            name = request.form.get('name')
            birthdate = request.form.get('birthdate')
            year = request.form.get('year')
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
            return render_template('index.html', js_folder=url_for('static', filename='js'),
                                   img_folder=url_for('static', filename='img'),
                                   css_folder=url_for('static', filename='css'),
                                   verif=1, veriferror=e)
    @classmethod
    def allowed_filename(cls, name):
        extension = name.split('.')[-1]
        if extension.lower() in ['png', 'jpg', 'jpeg']:
            return True
        else:
            return False

    def run(self, host, port):
        webapp.run(host, port)

if __name__ == '__main__':
    app = App()
    app.run('0.0.0.0', '5010')
