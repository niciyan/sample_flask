from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import english_word_app
from .forms import EnglishWordForm
from ..models import EnglishWord, db


@english_word_app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = EnglishWordForm()
    # print(len(form.word_input_forms.data), type(form.word_input_forms.data))
    if form.validate_on_submit():
        c = 0
        for i, input_form in enumerate(form.word_input_forms.entries):
            if input_form.word.data != "" and input_form.meaning.data != "":
                word_submitted = EnglishWord(
                    word=input_form.word.data,
                    meaning=input_form.meaning.data,
                    author_id=current_user.id
                )
                db.session.add(word_submitted)
                c += 1
        db.session.commit()
        if c == 0:
            flash("No word saved.", 'info')
        else:
            flash("{} words saved!".format(c), 'success')
        return redirect(url_for('.index'))
    words = EnglishWord.query.order_by(EnglishWord.timestamp.desc()).all()
    return render_template('english_word/index.html', form=form, words=words)
