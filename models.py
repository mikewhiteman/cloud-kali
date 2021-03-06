import datetime
import boto3
import secrets
import string
import uuid
import time
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(40), unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(60), default='unverified')

    def __init__(self, email, first_name, last_name, password):
        self.id = str(uuid.uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)
        self.role = 'unverified'

    def verify_hash(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

class Image(db.Model):
    __tablename__ = 'images'
    ami_id = db.Column(db.String(60), primary_key=True, unique=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(512))

class Kali(db.Model):
    __tablename__ = 'instances'
    instance_id = db.Column(db.String(60), primary_key=True, unique=True)
    user_id = db.ForeignKey('User.id')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    username = db.Column(db.String(30))
    password =db.Column(db.String(30))
    ip_address = db.Column(db.String(30))
    state = db.Column(db.String(30), default='live')
    
    def __init__(self, user_id):
        self.user_id = user_id
        self._generate_creds()
        self._create_instance()
        self._get_instance_data()

    def _generate_creds(self):
        alphabet = string.ascii_letters + string.digits
        self.username = 'cloudkali'
        self.password = ''.join(secrets.choice(alphabet) for i in range(12))

    def _create_instance(self):
        ec2 = boto3.resource('ec2')
        userdata = f"""#!/bin/bash
        ###
        # This script will provision an an account with a random password
        ###
        useradd -m -s /bin/bash {self.username}
        echo {self.username}:{self.password} |  chpasswd
        usermod -aG sudo {self.username}
        """
        
        ec2_instance = ec2.create_instances(
        ImageId='ami-0f24d5a5c0b5c0a18',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.small',
        KeyName='cis4093_kali_hosts',
        SecurityGroupIds=['sg-0eb2588803e7caef8'],
        UserData = userdata,
        SubnetId='subnet-021de55c66cc45ff3'
        )

        self.instance_id = ec2_instance[0].instance_id

    def _get_instance_data(self):
        time.sleep(3) #Quick hack since ec2 IP address takes a few seconds to gen. This will be async in the future.
        client = boto3.client('ec2')
        instance_data = client.describe_instances(InstanceIds=[self.instance_id])
        self.ip_address = instance_data['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']