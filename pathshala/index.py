from flask import Flask, render_template, request,session,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime
from flask_bcrypt import Bcrypt



with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key= 'my_secret_key'.encode('utf8')
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

class Users(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)

@app.route("/", methods=['GET','POST'])
def home():
    if ('user' in session):
        return render_template('index.html', params=params)

    else :
        return render_template('login-register.html')


@app.route("/test")
def test():
    
    return render_template('test.html', params=params)


@app.route("/register", methods=['POST','GET'])
def register():
    if(request.method=='POST'):
        form=RegistrationForm()
        if form.validate_on_submit():
            hashed_password=bcrypt/generate_password_hash(form.password.data).decode('utf8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has bee created','success')
            return redirect(url_for('login'))
        '''username=request.form.get('Username')
        password=request.form.get('Password')
        email=request.form.get('Email')
        entry = Users(username=username, password= password, email = email)
        db.session.add(entry)
        db.session.commit()
        return render_template('login-register.html', params=params)'''

    else:
        return render_template('login-register.html', params=params)

@app.route("/login", methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        Username=request.form.get('Username')
        Password=request.form.get('Password')
        asset=Users.query.all()
        for x in asset:
            print(str(x))
        if(Username==asset.username and Password==asset.password):
            session['user']=Username
            return render_template('dashboard.html', params=params)
        else:
            return render_template('test.html',params=params)

    else:
        [session.pop(key) for key in list(session.keys())]
        return render_template('login-register.html', params=params)


@app.route("/post/", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
	post = Posts.query.all()
	if(request.method=='GET'):
		return render_template('login.html', params=params)
	if ('user' in session and session['user']==params['admin_user']):
		return render_template('dashboard.html', params=params,posts=post)
	if(request.method=='POST'):
		uname = request.form.get('uname')
		password = request.form.get('pass')
		if(uname==params['admin_user'] and password==params['admin_password']):
			session['user']=uname
    
			return render_template('dashboard.html', params=params,posts=post)
		else:
			return render_template('login.html', params=params)
	 

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', params=params)


app.run(debug=True)