from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
# from wtforms.fields.core import RadioField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, user_logged_in

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretPakis3519'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/warga_1-7'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@database/warga_1-7'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/warga_1-7'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class DaftarWarga(db.Model):
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
    alias = db.Column(db.String(20))

    def __init__(self, nama, kota, tanggal, kelamin, nokk, nonik, alamatktp, kotaktp, anggota, bloki, norumah, statusrumah, rt, pekerjaan, phone, email, alias):
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
        self.alias = alias


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember_me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    new_psw1 = PasswordField('Password baru', validators=[InputRequired(), Length(min=8, max=80)])
    new_psw2 = PasswordField('Ulang password baru', validators=[InputRequired(), Length(min=8, max=80)])

# class DaftarForm(FlaskForm):
#     nama = StringField('Nama Lengkap', validators=[InputRequired(), Length(min=4, max=80)])
#     kota = StringField('Kota Lahir', validators=[InputRequired(), Length(min=4, max=80)])
#     tanggal = DateField('Tanggal Lahir', format='%d-%m-%Y')
#     kelamin = RadioField('Jenis Kelamin', choices=[('kelamin1', 'Laki-laki'), ('kelamin2', 'Perempuan')])
#     nokk = StringField('No KK', validators=[InputRequired(), Length(min=16, max=16)])
#     nonik = StringField('NIK', validators=[InputRequired(), Length(min=16, max=16)])
#     alamatktp = TextAreaField('Alamat KTP', validators=[InputRequired(), Length(min=4, max=200)])
#     kotaktp = StringField('Kota KTP', validators=[InputRequired(), Length(min=4, max=80)])
#     anggota = RadioField('Anggota KK', choices=[('satu', 'Kepala Keluarga'), ('dua', 'Istri'), ('tiga', 'Anak'), ('empat', 'Lainnya')])
#     bloki = RadioField('Tinggal di Blok i/_', choices=[('satu', '1'), ('dua', '2'), ('tiga', '3'), ('empat', '4'), ('lima', '5')])
#     norumah = IntegerField('No Rumah', validators=[InputRequired(), NumberRange(min=1, max=200)])
#     statusrumah = RadioField('Status Rumah', choices=[('milik', 'Rumah milik'), ('kontrak', 'Rumah kontrak')])
#     rt = RadioField('RT', choices=[('01', '1'), ('02', '2')])
#     pekerjaan = RadioField('Pekerjaan', choices=[('satu', 'ASN'), ('dua', 'Karyawan Swasta'), ('tiga', 'Wira Swasta'), ('empat', 'Pelajar/Mahasiswa'), ('lima', 'Lainnya')])
#     phone = StringField('Phone', validators=[InputRequired(), Length(min=6, max=20)])
#     email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     alias = StringField('Nama Panggilan', validators=[InputRequired(), Length(min=2, max=20)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('daftar'))
            return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            # return '<h1>New user has been added!</h1>'
            login_user(new_user)
            return redirect(url_for('daftar'))
        except Exception as e:
            return render_template('signup.html', form=form, message='User already exist.')

    return render_template('signup.html', form=form)

@app.route('/changepsw', methods=['GET', 'POST'])
@login_required
def changepsw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if check_password_hash(user.password, form.password.data):
            if form.new_psw1.data == form.new_psw2.data:
                if check_password_hash(user.password, form.new_psw1.data):
                    return render_template('changepsw.html', form=form, message='Password baru & lama identik')
                hashed_password = generate_password_hash(form.new_psw1.data, method='sha256')
                print('Current password: ' + user.password)
                user.password = hashed_password
                print('New password: ' + user.password)
                db.session.commit()
                return render_template('successchpsw.html')
            return render_template('changepsw.html', form=form, message='New password not confirmed')
        return render_template('changepsw.html', form=form, message='Invalid password')
    return render_template('changepsw.html', form=form)

@app.route('/daftar')
@login_required
def daftar():
    return render_template('daftar.html', name=current_user.username)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/wargalist')
def wargalist():
    tasks = DaftarWarga.query.order_by(DaftarWarga.nama).all()
    # tasks = db.session.query(DaftarWarga).all()
    return render_template('wargalist.html', tasks=tasks)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
@login_required
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
        alias = request.form['alias']

        if nama == '' or nokk == '' or nonik == '' or anggota == "" or norumah == '' or alias == '':
            return render_template('daftar.html', content='Silahkan masukan data lengkap kecuali phone dan email.')
            # return redirect(url_for('daftar'), Response='Silahkan masukan data lengkap kecuali phone dan email.')
        if db.session.query(DaftarWarga).filter(DaftarWarga.nama == nama).count() == 0:
            data = DaftarWarga(nama, kota, tanggal, kelamin, nokk, nonik, alamatktp, kotaktp, anggota, bloki, norumah, statusrumah, rt, pekerjaan, phone, email, alias)
            db.session.add(data)
            db.session.commit()
            # send_mail(nama, kota, tanggal, nokk, nonik, phone, email)
            return render_template('success.html')
        return render_template('daftar.html', content='Data sudah terdaftar!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='127.0.0.1', port=8080, debug=True)