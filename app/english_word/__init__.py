from flask import Blueprint

english_word_app = Blueprint('english_word', __name__)

from . import views
