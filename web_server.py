
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'collection'
app.config['MONGO_URI']='mongodb+srv://test:test@cluster0.kw4id.mongodb.net/collection?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
	if 'username' in session:
		return 'You are logged in as the following user:' +session['username']
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

	user = mongo.db.users
	login_user = user.find_one({'name' : request.form['username']})

	if login_user:
		if bcrypy.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	return 'Invalid username or password combination'

@app.route('/register', methods=['POST','GET'])
def register():
	if request.method == 'POST':
		users= mongo.db.users
		existing_user = users.find_one({'name': request.form['username']})

		if existing_user is None:
			hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			users.insert({'name':request.form['username'], 'password':hashpass})
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	return 'username already in database'

	return render_template(register.html)

if(__name__=='__main__'):
	app.secret_key='secretivekey'
	app.run(debug=True)
