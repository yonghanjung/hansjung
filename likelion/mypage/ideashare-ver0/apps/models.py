"""
models

"""

from apps import db


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
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())


