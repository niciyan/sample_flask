from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EnglishWordForm(FlaskForm):
    word = StringField('Word', validators=[Length(0, 200)])
    meaning = TextAreaField('Meaning')
    submit = SubmitField('Save')
