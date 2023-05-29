from datetime import timezone

from sqlalchemy.sql import func
from . import db
# import sqlite3



class Tasks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    data=db.Column(db.String(1000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100), unique=True)
    city=db.Column(db.String(100))
    country=db.Column(db.String(100))
    tasks=db.relationship('Tasks')
