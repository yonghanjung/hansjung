# -*- coding: utf-8 -*-

"""
models

"""

from apps import db

class User(db.Model):
    email = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default = db.func.now())


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    content = db.Column(db.Text())
    category = db.Column(db.String(255))
    data_created = db.Column(db.DateTime(), default=db.func.now())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    artlcle = db.relationship('Article',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    # Bidirection relationship
    '''
    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address", backref="user")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey('user.id'))
    '''
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    likecount = db.Column(db.Integer, default = 0, nullable = False)
    commentcheck = db.Column(db.Integer, default = 0, nullable = False)


