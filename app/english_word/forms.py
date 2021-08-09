from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import Length


class SubEnglishWordForm(FlaskForm):
    word = StringField('単語', validators=[Length(0, 200)])
    meaning = TextAreaField('意味')

    class Meta:
        csrf = False


class EnglishWordForm(FlaskForm):
    word_input_forms = FieldList(FormField(SubEnglishWordForm), min_entries=4, max_entries=10)
    submit = SubmitField('保存')
