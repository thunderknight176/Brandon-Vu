from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self,username,password):
        self.username=username
        self.password=password
    def __rep__(self):
        return f'<User: {self.username}>'