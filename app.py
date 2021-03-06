import os
import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from models import db, User, Kali, Image, login_manager
from forms import UserRegistrationForm, UserLoginForm

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = UserRegistrationForm()
    if registration_form.validate_on_submit():
        user = User(email=registration_form.email.data, first_name=registration_form.first_name.data, last_name=registration_form.last_name.data, password=registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Account is pending manual approval.')
        return redirect(url_for('register'))
    return render_template('register.html', form=registration_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = UserLoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_hash(login_form.password.data):
            login_user(user)
            print(f"[{datetime.datetime.utcnow()}] User {user.email} logged in")
        else:
            flash("Incorrect account credentials")
    return render_template('login.html', form=login_form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return "dashboard"

@app.route('/instance', methods=['POST'])
@login_required
def create_instance():
    user_id = current_user.id
    kali = Kali(user_id)
    db.session.add(kali)
    db.session.commit()
    return f"""[Debug] Created instance with the following info:

    instance_id = {kali.instance_id}
    username = {kali.username}
    password = {kali.password}
    ip_address = {kali.ip_address} """

if __name__ == '__main__':
    (app.run(host='0.0.0.0', debug=True))