import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import Bookmark, User
from ..forms import AddBookmark
from ..extensions import login_manager, db


api = Blueprint("api", __name__)
