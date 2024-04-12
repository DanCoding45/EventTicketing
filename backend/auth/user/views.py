from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from auth.user.forms import UserRegistrationForm, UserLoginForm
from auth.user.models import User
import sqlite3

auth = Blueprint("auth", __name__)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            conn = sqlite3.connect('database.db')

            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
        
            cursor = conn.cursor()        
            cursor.execute("INSERT INTO users (first_name, last_name, username, email, password) VALUES (?, ?, ?, ?, ?)",
                   (user.first_name, user.last_name, user.username, user.email, user.password))
            
            conn.commit()
            conn.close()
            
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid Form Data Provided. Please try again!")
    return render_template("auth/user/register.html", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0]
                session['username'] = user[3]
                session['logged_in'] = True

                conn.close()
                return redirect(url_for('event_guest.home'))
            else:
                flash("Invalid Credentials! Please try again!")
            
        else:
            flash("Invalid Form Data. Please try again!")
    
    return render_template("auth/user/login.html", form=form)

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('shopping_cart', None)

    return redirect(url_for('auth.login'))

