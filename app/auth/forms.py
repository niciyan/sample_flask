# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

from ..models import User


class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    remember_me = BooleanField('パスワードを記憶する')
    submit = SubmitField('ログイン')


class RegistrationForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Length(1, 64),
                                               Email()])
    username = StringField('ユーザー名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    password = PasswordField('パスワード', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('パスワード(確認用)', validators=[DataRequired()])
    submit = SubmitField('登録')

    # this method run automatically
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    # this method run automatically
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('前のパスワード', validators=[DataRequired(), Length(1, 64)])
    new_password = PasswordField('新しいパスワード', validators=[DataRequired(), Length(1, 64)])
    new_password2 = PasswordField('新しいパスワード(確認)', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('送信')

    def check_old_password(self, user):
        if not user.verify_password(self.old_password.data):
            self.old_password.errors.append('your password is wrong.')
            return False
        return True
