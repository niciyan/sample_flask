from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length

class NameForm(FlaskForm):
    text = StringField("your message", validators=[ Required(), Length(1, 40) ])
    submit = SubmitField('送信')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[ Length(0,64) ])
    location = StringField('Location', validators=[ Length(0,64) ])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
