from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3307/database'
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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


@app.route('/')
def home():
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

        return redirect('/')

    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
