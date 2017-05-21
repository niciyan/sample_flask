from flask import render_template, redirect, flash, url_for, current_app, abort
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Message, User
from .forms import NameForm, EditProfileForm
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = NameForm() 
    # if request.method == 'POST':
    if form.validate_on_submit():
        # form.text.data
        now = datetime.utcnow()
        me = Message(message=form.text.data, date=now, author=current_user._get_current_object())
        db.session.add(me)
        db.session.commit()
        flash('新しいメッセージを追加しました!!', 'success')
        current_app.logger.debug('new data inserted.')
        return redirect(url_for('.index'))
    return render_template('index.html',
            messages=Message().query.order_by(Message.date.desc()).limit(6).all(),
            users=User().query.all(),
            form=form)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('プロファイルが更新されました', 'success')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/ajax')
def load_ajax():
    messages = Message().query.filter_by(author_id=current_user.get_id()).order_by(Message.date.desc()).all()
    return render_template('ajax.html', messages=messages)

@main.route('/admin')
def show_users():
    users = User().query.all()
    return render_template('admin.html', users=users)

@main.route('/reminder')
def paginating():
    pagination = Message.query.order_by(Message.date.desc()).paginate(per_page=8, error_out=False)
    return render_template('page.html', pagination=pagination)
