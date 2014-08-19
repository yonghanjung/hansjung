# -*- coding: utf-8 -*-
from flask import render_template, request
from apps import app

@app.route('/', methods=['GET'])
def article_list():
    return render_template("home.html")

#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500