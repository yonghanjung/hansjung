# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, url_for, g
from apps import app, db
from apps.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
    # Otherwise, index.html loaded


@app.route('/join', methods=['GET', 'POST'])
def user_join():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        user = User(
            email=email,
            password=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.get(email)
        message = None

        if user is None:
            message = u'user가 존재하지 않습니다.'
        elif not check_password_hash(user.password, password):
            message = u'password가 잘못되었습니다.'
        else:
            session.permanent = True
            session['user_id'] = user.email
            session['user_name'] = user.name

            return redirect(url_for('main'))


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user_name = None
    if 'user_id' in session:
        g.user_name = session['user_name']
        
