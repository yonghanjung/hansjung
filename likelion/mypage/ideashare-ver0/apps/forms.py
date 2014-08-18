# -*- coding: utf-8 -*-
from flask.ext.wtf import Form


__author__ = 'jeong-yonghan'


from wtforms import (
    StringField,
    PasswordField,
    TextAreaField
)
from wtforms import validators
from wtforms.fields.html5 import EmailField

class ArticleForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description = {'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'이름을 입력하세요.'}
    )
    category = StringField(
        u'카테고리',
        [validators.data_required(u'카테고리를 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'카테고리를 입력하세요.'}
    )

class CommentForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description = {'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'이름을 입력하세요.'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'비밀번호를 입력하세요.'}
    )

    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'이메일을 입력하세요.'}

    )


class JoinForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder' : u'이메일을 입력하세요'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다. '),
         validators.EqualTo('confirm_password', message= u'패스워드가 일치하지 않습니다.')],
        description = {'placeholder' : u'패스워드를 입력하세요.'}
    )
    confirm_password = PasswordField(
        u'패스워드 확인',
        [validators.data_required(u'패스워드를 한 번 더 입력하세요.')],
        description={'placeholder' : u'패스워드를 한 번 더 입력하세요'}
    )
    name = StringField(
        u'이름',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder' : u'이름을 입력하세요'}
    )


class LoginForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder' : u'이메일을 입력하세요'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다. ')],
        description = {'placeholder' : u'패스워드를 입력하세요.'}
    )