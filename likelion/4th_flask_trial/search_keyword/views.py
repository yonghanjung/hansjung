from flask import render_template, Flask, request
from apps import app


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    get = None
    post = None

    if request.args:
        get = request.args['text_get']

    if request.form:
        post = request.form['text_post']

    return render_template("index.html",
                           variable_get=get, variable_post=post)

    #age = 21
    #species = "lion"
    #friend = ["google", "teacher", "student"]

    # return render_template("index.html", age=age, species=species,
    # friend=friend)

    # Declare variables in Python, and then transfer variables to the 'index.html' file
    # We need a html syntax to make html file to communicate with Python file

    # ========================================================================#
    # In summary, we takes input in HTML.
        # At first, we takes input as type of 'get'
        # At second, we takes input as type of 'post'
        # Then, in Python file, by the command of request.args['text_get'],
        # we obtains 'get' variable, in same way, we obtain 'post' variable
        # Then, as we knew at the very first, we again transfer the value we obtained in Python
        # to the index.html
