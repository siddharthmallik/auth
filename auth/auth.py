from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'collection'
app.config['MONGO_URI']='mongodb+srv://test:test@cluster0.kw4id.mongodb.net/collection?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('app.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('app.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('app.login'))

if(__name__=='__main__'):
    app.secret_key='secretivekey'
    app.run(debug=True)
