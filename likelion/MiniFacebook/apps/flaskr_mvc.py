# -*- coding: utf-8 -*-
# all the imports

from flask import request, redirect, url_for,\
    render_template
from apps import app
from database import Database
from google.appengine.ext import db



dataStorage = Database()


@app.route('/', methods=['GET', 'POST'])
def show_entries():
    entries = dataStorage.out()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    storage = {}
    storage['id'] = dataStorage.newid()
    storage['title'] = request.form['title']
    storage['contents'] = request.form['contents']
    storage['likecount'] = 0

    photo_data = request.files['photo']
    filestream = photo_data.read()
    storage['photo'] = db.Blob(filestream)

    dataStorage.put(storage)
    return redirect(url_for('show_entries'))

@app.route('/show/<key>', methods = ['GET'])
def shows(key):
    myphoto = dataStorage.select(key)
    myphoto_data = myphoto['photo']  
    return app.response_class(myphoto_data)

@app.route('/del/<key>', methods=['GET'])
def del_entry(key):  # File upload
    dataStorage.delete(key)
    return redirect(url_for('show_entries'))


@app.route('/like/<key>', methods=['GET'])
def like_entry(key):  # File upload
    data = dataStorage.select(key)
    data['likecount'] += 1
    dataStorage.update(key, data)

    return redirect(url_for('show_entries'))

@app.route('/dislike/<key>', methods=['GET'])
def dislike_entry(key):  # File upload
    data = dataStorage.select(key)
    data['likecount'] -= 1
    if data['likecount'] < 0:
        data['likecount'] = 0
    dataStorage.update(key, data)

    return redirect(url_for('show_entries'))


@app.route('/edit/<key>', methods=['GET'])
def edit_showbox(key):
    # SELECT the file by ID number
    # ACCESS to the file, title & content
    # gives the new value and update
    data = dataStorage.select(key)
    data['check'] = 1
    return redirect(url_for('show_entries'))

@app.route('/editing/<key>', methods=['GET', 'POST'])
def editing(key):
    data = dataStorage.select(key)
    data['check'] = 0
    data['title'] = request.form['edit_title']
    data['contents'] = request.form['edit_contents']
    dataStorage.update(key, data)
    return redirect(url_for('show_entries'))
