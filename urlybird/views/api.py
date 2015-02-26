from flask import Blueprint, jsonify
from urlybird.models import Bookmark

api = Blueprint('api', __name__)

@api.route("/bookmarks")
def bookmarks():
    bookmarks = Bookmark.query.all()
    bookmarks = [bookmark.to_dict() for bookmark in bookmarks]
    return jsonify({"books": books})

@api.route("/books/<int:id>")
def bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    return jsonify(bookmark.to_dict())
