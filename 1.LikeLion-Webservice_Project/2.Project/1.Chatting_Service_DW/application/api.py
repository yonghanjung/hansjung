# -*- coding: utf-8 -*-

from pusher import Pusher
from application import app
# from flask import request, render_template, jsonify
# 이렇게 바꾸자
from flask import request, render_template, jsonify, session
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET
from sqlalchemy import exc as sqlalchemy_exceptions

p = Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET', 'POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message': data['message']})
    return jsonify({"status": 0})


# 이게 무슨 함수인지는 나중에 공부하자. 
def emit(action, data, broadcast=False):
    if broadcast:
        p['br'].trigger(action, data)
    else:
        p['private'].trigger(action, data)


def emit_new_message(data):
    # emit('new_message', {'message' : data['message'] }, broadcast = True)
    emit('new_message', {
         'message': data['message'],
         'username': data['username'],
     }, broadcast=True)


@app.route('/api/start', methods=["POST"])
def api_start():
    data = request.form
    username = data['username']

    # 다음 추가 
    user_id = data['user_id']
    session['username'] = username
    session['user_id'] = user_id

    emit('user_joined', {'username': username}, broadcast=True)

    return jsonify({'status': 0})


# --------

@app.route('/api/call/<action_name>', methods=["POST"])
def api_call(action_name):
    data = request.form

    # emit_new_message(data)
    # 이 부분 추가하자 

    if action_name == "new_message":
        emit_new_message(data)
    elif action_name == "typing":
        emit_typing()
    elif action_name == "stop_typing":
        emit_stop_typing()

    return jsonify({"status": 0})

# Typing 인식하는 함수 만들자 
def emit_typing():
    emit('typing', {
        'username': session['username'],
        'user_id': session['user_id'],
    }, broadcast=True)


def emit_stop_typing():
    emit('stop_typing', {
        'username': session['username'],
        'user_id': session['user_id'],
    }, broadcast=True)