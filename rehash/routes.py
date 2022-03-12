import os
from flask import render_template, redirect, url_for, flash, request
from rehash import app, bcrypt, mail, db
from rehash.forms import LoginForm, SignupForm, SummarizeForm
from rehash.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.utils import secure_filename
import PyPDF2
import docx

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')			
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
           return render_template('login.html',form=form)
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, occupation=form.occupation.data)
        db.session.add(user)
        db.session.commit()
        #flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/summarize',methods=['GET', 'POST'])
def summarize():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    form = SummarizeForm()
    if form.validate_on_submit():
        text = form.text.data
        if text == None:
            print(text[:25])
        else :
            upload = request.files['file']
            this_path = os.path.join("E:\\rehash\\rehash\\static\\files", secure_filename(upload.filename))
            upload.save(this_path)
            result = ""
            if(this_path[-3:]=='txt'):
                with open(this_path, 'r') as ftxt:
                    content = ftxt.readlines()
                for i in content:
                    result+=i[:-1]+" "
            elif this_path[-3:]=='pdf':
                obj = open(this_path,'rb')
                reader = PyPDF2.PdfFileReader(obj)
                numPages = reader.numPages
                result1 = ""
                for i in range(0,numPages):
                    pageObj = reader.getPage(i)
                    print(type(pageObj.extractText()))
                    result1+=pageObj.extractText() + " "
                obj.close()
                for i in result1:
                    if i == '\n':
                        result += ""
                    else:
                        result += i
            else:
                doc = docx.Document(this_path)  # Creating word reader object.
                fullText = []
                for para in doc.paragraphs:
                    fullText.append(para.text)
                    result = ' '.join(fullText)
            print(result)
        #flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
        return redirect(url_for('summarize'))
    return render_template('summarize.html',form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))