from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import english_word_app
from .forms import EnglishWordForm
from ..models import EnglishWord, db


@english_word_app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = EnglishWordForm()
    if form.validate_on_submit():
        word_submitted = EnglishWord(
            word=form.word.data,
            meaning=form.meaning.data,
            author_id=current_user.id
        )
        db.session.add(word_submitted)
        db.session.commit()
        flash("new word saved!", 'success')
        return redirect(url_for('.index'))
    words = EnglishWord.query.order_by(EnglishWord.timestamp.asc()).all()
    return render_template('english_word/index.html', form=form, words=words)
