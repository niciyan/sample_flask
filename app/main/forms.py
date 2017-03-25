from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    text = StringField("your message", validators=[ Required() ])
    submit = SubmitField('送信')

