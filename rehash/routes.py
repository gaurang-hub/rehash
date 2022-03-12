from flask import render_template, redirect, url_for, flash, request
from rehash import app, bcrypt, mail, db
from rehash.forms import LoginForm, SignupForm
from rehash.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


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
           return render_template('login.html')
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
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))