__author__ = 'jeong-yonghan'

from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from apps import app, db
from apps.forms import ArticleForm, CommentForm, JoinForm
from apps.models import (
    Article,
    comment,
    user
)

@app.route('/user/join', methods = ['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email = form.email.data,
                password = generate_password_hash(form.password.data),
                name = form.name.data
            )
            db.session.add(user)
            db.session.commit()

            flash(u'가입이 완료되었습니다.', 'success')
            return redirect(url_for('article_list'))
    return render_template('user/join.html', form = form, active_tab = 'article_create')