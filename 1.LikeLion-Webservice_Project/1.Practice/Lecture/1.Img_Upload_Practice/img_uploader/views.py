from flask import render_template, Flask, url_for, request
from apps import app

from google.appengine.ext import db


class Photo(db.Model):
    photo = db.BlobProperty()
    # class Photo is defined.


@app.route('/')
@app.route('/index')
def index():
    return render_template('upload.html')
    # When users first visits the website, users
    # will see 'upload.html'


@app.route('/upload', methods=['POST'])
def upload_db():
    post_data = request.files['photo']
    # request module enable us to load input in html
    # request module is pair with 'form' data.
    # User uploads file, and names it 'photo', and once users
    # click 'submit', it transfer to 'post_data'

    filestream = post_data.read()
    # When Python loads a file, we should command Python to read it

    upload_data = Photo()
    # This is an instance created by calling Photo.
    # the role of upload_data is to call 'BlobProperty'

    upload_data.photo = db.Blob(filestream)
    # It is the command that we upload the filestream to the GAE

    upload_data.put()
    # Then, upload filestream to the GAE database.

    url = url_for("show", key=upload_data.key())
    # When putting filestream to the GAE database,
    # the key for a filestream created.
    # We can call that filestream by this 'key'
    # This url points that filestream specifically.

    # This is how to use  'url_for'
        # the module url_for generates the url to the given methods.
        # url_for("show") creates the url to the 'show' funciton
        # url_for("upload_db") creates the url to the upload_db

    return render_template("upload.html", url=url)
    # Then gives this url with key to the upload.html


@app.route('/show/<key>', methods=['GET'])
def show(key):
    upload_data = db.get(key)
    # We gives the 'key' to the showing function.
    # Then the variable 'upload_data' points that filestream with 'key'
    return app.response_class(upload_data.photo)
    # return this data as the photo.
