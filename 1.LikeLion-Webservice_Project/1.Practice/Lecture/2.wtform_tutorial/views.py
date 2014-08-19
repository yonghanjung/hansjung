from flask import render_template, Flask, request
from apps import app

from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
SubmitField, validators, ValidationError

# ContactForm is a class of textfields taking input of personal information


class ContactForm(Form):
    name = TextField("name", [validators.Required("Please enter your name.")])
    email = TextField(
        "Email", [validators.Required("Please enter your email address"), validators.Email("Please enter valid email address")])

    subject = TextField(
        "Subject", [validators.Required("Please enter a subject")])
    message = TextAreaField(
        "Message", [validators.Required("Please enter a message")])
    submit = SubmitField("send")


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    form = ContactForm()

    # We already import 'request' library
    # form.validate is already offered by library
    if request.method == "POST":
        if form.validate() == False:
            return render_template("index.html", form=form)
        else:
            return "Nice to meet you, " + form.email.data + "!"

    return render_template("index.html", form=form)
