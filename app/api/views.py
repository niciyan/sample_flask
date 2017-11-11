from flask import jsonify
from ..models import Message
from . import api

@api.route('/posts')
def get_posts():
    messages = Message.query.limit(100).all()
    return jsonify({ 'messages': [ message.to_json() for message in messages ] })
