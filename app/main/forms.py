# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField

class MessageForm(FlaskForm):
    body = PageDownField(
            "下に変換されたテキストが描画されます", 
            default="# Title\nParagraph.\n\n    this is code block(with 4 spaces)\n    happy coding!\n\n*italic block*\n\n**bold string**", 
            validators=[ Required() ]
            )
    submit = SubmitField('送信')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[ Length(0,64) ])
    location = StringField('Location', validators=[ Length(0,64) ])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = StringField('あなたのコメント', validators=[Required()])
    submit = SubmitField('送信')
