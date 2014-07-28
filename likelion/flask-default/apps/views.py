from flask import render_template, Flask, url_for, request
from apps import app

from google.appengine.ext import db


class Upload(db.Model):
    blogtext = db.StringProperty(multiline=True)
    photo = db.BlobProperty()
    

@app.route('/')
@app.route('/index')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_db():
    post_data = request.form['blog']
    photo_data = request.files['photo']
    filestream = photo_data.read()

    upload_data = Upload()
    upload_data.photo = db.Blob(filestream)

    upload_data.put()

    url = url_for("show", key=upload_data.key())

    return render_template("upload.html", texttext = post_data, url = url)
    # Then gives this url with key to the upload.html

@app.route('/show/<key>', methods=['GET'])
def show(key):
    upload_data = db.get(key)
    # We gives the 'key' to the showing function.
    # Then the variable 'upload_data' points that filestream with 'key'
    return app.response_class(upload_data.photo)
    # return this data as the photo.


