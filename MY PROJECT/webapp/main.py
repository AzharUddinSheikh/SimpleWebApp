from flask import Flask, render_template, request, redirect, abort, session, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['localserver']
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = params['uploadlocation']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'azharsheikh760@gmail.com',
    "MAIL_PASSWORD": 'Valar123@'
}

app.config.update(mail_settings)
mail = Mail(app)


class Details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __inti__(self, username, email, phone, name, password):
        self.name = name
        self.email = email
        self.username = username
        self.phone = phone
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
    if ('user' in session and session['user'] == params['adminusername']):
        return render_template('dashboard.html', params=params)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (username == params['adminusername'] and password == params['adminpassword']):
            session['user'] = username
            return render_template('dashboard.html', params=params)

        else:
            abort(500)

    return render_template('login.html')


@app.route('/create', methods=['GET', 'POST'])
def createnew():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')

        entry = Details(name=name, email=email, username=username,
                        phone=phone, password=password)
        db.session.add(entry)
        db.session.commit()

        msg = Message('New SIGN UP from BLOG', sender=email,
                      recipients=[params['myemail']], body=phone)

        mail.send(msg)

        return redirect('/')

    return render_template('create.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if ('user' in session and session['user'] == params['adminusername']):
        if request.method == "POST":
            f = request.files['file']
            f.save(os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

            return "uploaded successfully"


if __name__ == "__main__":
    app.run(debug=True)
