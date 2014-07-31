# -*- coding : utf-8 -*-

from flask import Flask, render_template, request, flash, abort, url_for, current_app
from apps import app
from google.appengine.ext import db


class Photo(db.Model):
    photo = db.BlobProperty()
    blogtext = db.StringProperty()


@app.route('/')
@app.route('/index')
def index():
    return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload():
    myfile = request.files['photo']
    mytxt = request.form['blog']

    if myfile:
        filestream = myfile.read()

    photo = Photo()
    photo.photo = db.Blob(filestream)
    photo.put()
    photo_url = url_for(".show", key=photo.key())

    return render_template("upload.html", photo_url=photo_url)


@app.route('/show/<key>', methods=["GET"])
def show(key):
    photo = db.get(key)
    if not photo:
        return abort(404)
    else:
        mimetype = "image/png"
        return current_app.response_class(photo.photo, mimetype=mimetype)
