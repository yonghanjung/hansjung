# -*- coding: utf-8 -*-
import pusher
from application import app
from flask import render_template, request, jsonify
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = pusher.Pusher(
  app_id= PUSHER_APP_ID,
  key= PUSHER_KEY,
  secret= PUSHER_SECRET
)


@app.route('/api/echo', methods = ['GET', 'POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message': data['message']})
    return jsonify({"status": 0})