from flask import Flask,render_template, url_for, flash, redirect, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
import re
from datetime import datetime

from pathshala import app, db, bcrypt
from pathshala.forms import RegistrationForm, LoginForm
from pathshala.sentiment_analysis import Sentiment
from pathshala.models import User, Post,Playlist,Comments,Videos,Contacts
from flask_login import login_user, current_user, logout_user, login_required

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)

local_server = False
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
@app.route("/") 
@app.route("/home")
def home():
    playlists = Playlist.query.filter_by()
    return render_template('index.html', params=params, playlists=playlists)
session['type']=''
@app.route("/videos", methods=['GET','POST'])
def post_comment():
    try:
        postcomment = request.args.get('postcomment').strip()
        slug = request.args.get('slug')
        print(postcomment)
        params['id']=slug.split("-")[len(slug.split("-"))-1]
        params['slug']=slug.replace("-"+params['id'],"")
        playlists = Playlist.query.filter_by(slug=params['slug']).first()
        if postcomment:
            video = Videos.query.filter_by(sno=playlists.sno)
            entry=Comments(ID=video[int(params['id'])-1].ID,user=session['user'],comment=postcomment)
            db.session.add(entry)
            db.session.commit()
        
        print(params['slug'])
        if playlists:
            video = Videos.query.filter_by(sno=playlists.sno)
            comment = Comments.query.filter_by(ID=video[int(params['id'])-1].ID)
            params['comments']=comment.count()
            params['id']=int(params['id'])-1
            params['title']=' '.join(x.capitalize() or params['id'] for x in params['slug'].split('-'))
            return render_template('post.html', slug=slug,params=params,videos=video,comments=comment)
        return render_template('test.html', params=params)
    except Exception as e:
        # raise e
        playlists = Playlist.query.filter_by()
        return render_template('playlist.html',playlists=playlists ,params=params)


@app.route("/videos/<string:slug>", methods=['GET','POST'])
def post_route(slug):
    try:
        params['id']=slug.split("-")[len(slug.split("-"))-1]
        params['slug']=slug.replace("-"+params['id'],"")
        print(params['slug'])
        playlists = Playlist.query.filter_by(slug=params['slug']).first()
        if playlists:
            video = Videos.query.filter_by(sno=playlists.sno)
            comment = Comments.query.filter_by(ID=video[int(params['id'])-1].ID)
            params['comments']=comment.count()
            params['id']=int(params['id'])-1
            params['title']=' '.join(x.capitalize() or params['id'] for x in params['slug'].split('-'))
            return render_template('videos.html', slug=slug,params=params,videos=video,comments=comment)
        return render_template('/templates/404.html', params=params)
    except Exception as e:
        raise e
        print('###########=======================')
        return render_template('/templates/404.html', params=params)
        # raise e
    

@app.route("/test",methods=(['GET']))
def about():
    return render_template('test.html',params=params, title='About')

@app.route("/myaccount",methods=(['GET']))
def myaccount():
    return render_template('myaccount.html', params=params, title='update')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,type='student')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    print("opening register.html")
    return render_template('register.html',params=params, title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print('type ',session['type'])
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            print("Login Unsuccessful "+str())
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',params=params, title='Login', form=form)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('description')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Pathshala: New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
        redirect(url_for('contact'))
        print('method contact ',request.method)
    return render_template('contact.html', params=params)

@app.route("/report")
def report():
    try:
        model = request.args.get('log_model')
        train=request.args.get('train')
        comments_DT=Comments.query.filter_by()
        print('model ',model)
        SA=Sentiment()
        obj=SA._SA(comments_DT,model=model,train_size=float(train),)
        params['accuracy_score']=str(obj[1])
        Confusion_matrix=str(str(obj[2]))
        out=obj[3]
        print(list(filter(None,' '.join(re.split('[^0-9]',Confusion_matrix)).split(' '))))
        Confusion_matrix=list(filter(None,' '.join(re.split('[^0-9]',Confusion_matrix)).split(' ')))
        CLASSIFICATION_REPORT=str(obj[0]).split('\n')
        params['class-0']=' '.join(CLASSIFICATION_REPORT[2].split()).split(' ')
        params['class-1']=' '.join(CLASSIFICATION_REPORT[3].split()).split(' ')
        params['micro avg']=' '.join(CLASSIFICATION_REPORT[5].split()).split(' ')
        params['macro avg']=' '.join(CLASSIFICATION_REPORT[6].split()).split(' ')
        params['weighted avg']=' '.join(CLASSIFICATION_REPORT[7].split()).split(' ')
        return render_template('/report.html',confusion=Confusion_matrix, params=params, out=out)
    except Exception as e:
        raise(e)
        return render_template('/templates/404.html', params=params)


@app.route("/addplaylist",methods=['GET','POST'])
@login_required
def addplaylist():
    if(request.method=='POST'):
        subject = request.form.get('sub')
        intro = request.form.get('intro')
        playlist=Playlist.query.filter_by(title=subject).first()
        if not playlist:
            entry = Playlist(title=subject,slug=subject.replace(' ','-'),tagline=intro)
            db.session.add(entry)
            db.session.commit()
        else :
            print('Already present')
        topics = request.form.getlist('Topic')
        link = request.form.getlist('link')
        playlist=Playlist.query.filter_by(title=subject).first()
        i=0
        for topic in topics:
            if topic:
                same_video=Videos.query.filter_by(sno=playlist.sno ,title=topic).first()
                if not same_video:
                    entry = Videos(sno=playlist.sno,title=topic,link=link[i])
                    db.session.add(entry)
                    db.session.commit()
                    print('adding new video ',topic)
            i=i+1

        redirect(url_for('addplaylist'))
    elif session['type']=='admin':
        return render_template('/templates/add-playlist.html', params=params)
    else :
        return render_template('/templates/404.html', params=params)

@app.route("/<string:mypage>")
def mypage(mypage):
    try:
        if mypage!='bar-charts.html' or mypage!='add-playlist.html':
            comments_DT=Comments.query.filter_by()
            SA=Sentiment()
            obj=SA._SA(comments_DT,model='')
            params['accuracy_score']=str(obj[1])
            Confusion_matrix=str(str(obj[2]))
            print(list(filter(None,' '.join(re.split('[^0-9]',Confusion_matrix)).split(' '))))
            Confusion_matrix=list(filter(None,' '.join(re.split('[^0-9]',Confusion_matrix)).split(' ')))
            CLASSIFICATION_REPORT=str(obj[0]).split('\n')
            params['class-0']=' '.join(CLASSIFICATION_REPORT[2].split()).split(' ')
            params['class-1']=' '.join(CLASSIFICATION_REPORT[3].split()).split(' ')
            params['micro avg']=' '.join(CLASSIFICATION_REPORT[5].split()).split(' ')
            params['macro avg']=' '.join(CLASSIFICATION_REPORT[6].split()).split(' ')
            params['weighted avg']=' '.join(CLASSIFICATION_REPORT[7].split()).split(' ')
            return render_template('/templates/'+mypage,confusion=Confusion_matrix, params=params, title='Mypage')
        else :
            return render_template('/templates/404.html', params=params)
    except Exception as e:
        raise(e)
        return render_template('/templates/404.html', params=params)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', params=params, title='Account')
