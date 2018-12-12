# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

from ..models import User


class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('パスワード', validators=[Required()])
    remember_me = BooleanField('パスワードを記憶する')
    submit = SubmitField('ログイン')


class RegistrationForm(FlaskForm):
    email = StringField('メールアドレス', validators=[Required(), Length(1, 64),
                                               Email()])
    username = StringField('ユーザー名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('パスワード', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('パスワード(確認用)', validators=[Required()])
    submit = SubmitField('登録')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
