from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/warga_1-7'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200), unique=True)
    kota = db.Column(db.String(200))
    tanggal = db.Column(db.Date())
    nokk = db.Column(db.String(16))
    nonik = db.Column(db.String(16), unique=True)
    alamatktp = db.Column(db.String(200))
    kotaktp = db.Column(db.String(200))
    anggota = db.Column(db.String(20))
    kelamin = db.Column(db.String(20))
    bloki = db.Column(db.Integer)
    norumah = db.Column(db.Integer)
    statusrumah = db.Column(db.String(20))
    rt = db.Column(db.Integer)
    pekerjaan = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80))

    def __init__(self, nama, kota, tanggal, kelamin, nokk, nonik, alamatktp, kotaktp, anggota, bloki, norumah, statusrumah, rt, pekerjaan, phone, email):
        self.nama = nama
        self.kota = kota
        self.tanggal = tanggal
        self.kelamin = kelamin
        self.nokk = nokk
        self.nonik = nonik
        self.alamatktp = alamatktp
        self.kotaktp = kotaktp
        self.anggota = anggota
        self.bloki = bloki
        self.norumah = norumah
        self.statusrumah = statusrumah
        self.rt = rt
        self.pekerjaan = pekerjaan
        self.phone = phone
        self.email = email


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/daftar')
def home():
    return render_template('daftar.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nama = request.form['name']
        kota = request.form['kota']
        tanggal = request.form['date']
        kelamin = request.form['kelamin']
        nokk = request.form['no_kk']
        nonik = request.form['no_nik']
        alamatktp = request.form['alamatktp']
        kotaktp = request.form['kotaktp']
        anggota = request.form['anggota']
        bloki = request.form['blok_i_']
        norumah = request.form['no_rumah']
        statusrumah = request.form['status_rumah']
        rt = request.form['rt']
        pekerjaan = request.form['pekerjaan']
        phone = request.form['phone']
        email = request.form['email']
        # print(nama, kota, tanggal, nokk, nonik, anggota, kelamin)
        # print("Blok i /", bloki, "No.", norumah, rt, pekerjaan, phone, email)
        if nama == '' or nokk == '' or nonik == '' or anggota == "" or norumah == '':
            return render_template('daftar.html', message='Silahkan masukan data lengkap kecuali phone dan email.')
        if db.session.query(Feedback).filter(Feedback.nama == nama).count() == 0:
            data = Feedback(nama, kota, tanggal, kelamin, nokk, nonik, alamatktp, kotaktp, anggota, bloki, norumah, statusrumah, rt, pekerjaan, phone, email)
            db.session.add(data)
            db.session.commit()
            send_mail(nama, kota, tanggal, nokk, nonik, phone, email)
            return render_template('success.html')
        return render_template('daftar.html', message='Data anda sudah ada!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
