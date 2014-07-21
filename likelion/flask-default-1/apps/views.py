from flask import render_template, Flask
from apps import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"