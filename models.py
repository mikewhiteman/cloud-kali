import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(40), unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(60), default='Unverified')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_hash(self, password):
        check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Image(db.Model):
    __tablename__ = 'images'
    ami_id = db.Column(db.String(60), primary_key=True, unique=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(512))

class Instance(db.Model):
    __tablename__ = 'instances'
    instance_id = db.Column(db.String(60), primary_key=True, unique=True)
    user_id = Column(db.String(60), ForeignKey('User.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    username = Column(db.String(30))
    password = Column(db.String(30))
    state = Column(db.String(30), default='live')




