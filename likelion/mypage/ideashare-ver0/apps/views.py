# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash
from apps.forms import ArticleForm, CommentForm
from apps import app, db
from sqlalchemy import desc
from apps.models import Article, Comment


@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.data_created)).all()
    return render_template("home.html", context=context, active_tab="timeline")


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            article = Article(
                title=form.title.data,
                author=form.author.data,
                category=form.category.data,
                content=form.content.data
            )

            db.session.add(article)
            db.session.commit()

            flash(u'게시물을 작성하였습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)
    comment = Comment.query.order_by(desc(Comment.date_created)).all()
    return render_template('article/detail.html', article=article, comments=comment)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.commit()
        return redirect(url_for('article_detail', id=id))
    return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html', article_id=id)
    elif request.method == 'POST':
        article_id = request.form['article_id']
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()

        flash(u'게시물을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))


@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                #article=Article.query.get(article_id)
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'댓글을 작성하였습니다', 'success')
        return redirect(url_for('article_detail', id=article_id))
    return render_template('comment/create.html', form=form)


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