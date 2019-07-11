# -*- coding: utf-8 -*-
from flask import request
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class MessageForm(FlaskForm):
    body = PageDownField(
        "下に変換されたテキストが描画されます",
        default="### Title\nParagraph. *italic block* **bold string**\n\n    this is code block(with 4 spaces)\n    happy coding!\n\n",
        validators=[DataRequired()]
    )
    submit = SubmitField('送信')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('あなたのコメント', validators=[DataRequired()])
    submit = SubmitField('送信')


class SearchForm(FlaskForm):
    q = StringField('検索', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
