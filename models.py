#encoding: utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(25),nullable=False)
    password = db.Column(db.String(30),nullable=False)

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('videos'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    video = db.relationship('Video',backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('answers'))



