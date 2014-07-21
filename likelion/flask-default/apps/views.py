from flask import render_template, Flask, request
from apps import app

import urllib2
from bs4 import BeautifulSoup


def crawler(url):
    source = urllib2.urlopen(url).read()\
        .decode('utf-8', 'ignore')
    soup = BeautifulSoup(source)
    return soup


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/crawl', methods=["GET", "POST"])
def crawl():
    dcurl = "http://gall.dcinside.com/board/lists/?id=" + \
        request.form['id'] + "&page=" + request.form['page']

    soup = crawler(dcurl)

    context = soup.findAll('td', attrs={'class': 't_subject'})

    result = ""

    for each in context:
        if each.a.string:
            result += each.a.string + "<br>"

    return result


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
