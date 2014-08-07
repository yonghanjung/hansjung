"""
Initialize Flask app

"""
from flask import Flask


app = Flask('apps')
app.config.from_object('apps.settings.Production')

import views