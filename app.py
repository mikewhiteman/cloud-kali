import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Kali, Image, login_manager

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)

@app.route('/') 
def home():
    return render_template('home.html')

if __name__ == '__main__':
    (app.run(host='0.0.0.0', debug=True))