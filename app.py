import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, login_manager
from kali_management import create_instance

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)

@app.route('/portal')
def portal():
    return render_template('portal.html')

if __name__ == '__main__':
    (app.run(host='0.0.0.0', debug=True))