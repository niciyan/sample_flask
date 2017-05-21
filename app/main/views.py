from flask import render_template, redirect, flash, url_for, current_app, abort
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Message, User, Comment
from .forms import MessageForm, EditProfileForm
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm() 
    # if request.method == 'POST':
    if form.validate_on_submit():
        # form.text.data
        now = datetime.utcnow()
        me = Message(body=form.body.data, date=now, author=current_user._get_current_object())
        db.session.add(me)
        db.session.commit()
        flash('新しいメッセージを追加しました!!', 'success')
        current_app.logger.debug('new data inserted.')
        return redirect(url_for('.index'))
    pagination = Message.query.order_by(Message.date.desc()) \
            .paginate(per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], \
            error_out=False)
    messages=pagination.items
    return render_template('index.html',
            pagination=pagination,
            messages=messages,
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

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    message = Message.query.get_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                post=post,
                author=current_user._get_current_object())
        db.session.add(comment)
        flash('コメントが公開されました！')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
                current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).pagenate(
            page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False
            )
    return render_template('post.html', form=form, pagination=pagination)


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
        flash('The message has been updated.')
        return redirect(url_for('.post', id=message.id))
    form.body.data = message.body
    return render_template('edit_post.html', form=form)
