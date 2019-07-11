# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, redirect, flash, url_for, current_app, abort, request, g
from flask_login import login_required, current_user

from . import main
from .forms import MessageForm, EditProfileForm, CommentForm, SearchForm
from .. import db
from ..models import Message, User, Comment


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@main.route('/', methods=['GET'])
def index():
    pagination = Message.query.order_by(Message.date.desc()) \
        .paginate(per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], \
                  error_out=False)
    messages = pagination.items
    return render_template('index.html',
                           pagination=pagination,
                           messages=messages
                           )


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = MessageForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('sign in to submit your message.', 'info')
            return redirect(url_for('auth.login'))
        # form.text.data
        now = datetime.utcnow()
        me = Message(body=form.body.data, date=now, author=current_user._get_current_object())
        db.session.add(me)
        db.session.commit()
        flash('新しいメッセージを追加しました!!', 'success')
        current_app.logger.debug('new data inserted.')
        return redirect(url_for('.index'))
    return render_template('create.html', form=form)


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


@main.route('/admin')
def show_users():
    users = User().query.all()
    return render_template('admin.html', users=users)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    message = Message.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('sign in to submit your comment.', 'info')
            return redirect(url_for('auth.login'))
        comment = Comment(body=form.body.data,
                          message=message,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('コメントが公開されました！', "success")
        return redirect(url_for('.post', id=message.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (message.comments.count() - 1) / \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = message.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('post.html', form=form, messages=[message], comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    message = Message.query.get_or_404(id)
    if current_user != message.author:
        abort(403)
    form = MessageForm()
    if form.validate_on_submit():
        message.body = form.body.data
        db.session.add(message)
        flash('メッセージが更新されました!', "success")
        return redirect(url_for('.post', id=message.id))
    form.body.data = message.body
    return render_template('edit_post.html', form=form)


@main.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.msearch(g.search_form.q.data) \
        .paginate(per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    messages = pagination.items

    return render_template('search.html', messages=messages, next_url=None, prev_url=None)
