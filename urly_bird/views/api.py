from flask import Blueprint, jsonify
from urly_bird.models import Link

api = Blueprint("api", __name__)

@api.route("/links")
def links():
    links = Link.query.all()
    links = [link.to_dict() for link in links]
    return jsonify({'links': links})

@api.route('/links/<int:id>')
def link(id):
    link = Link.query.get_or_404(id)
    return jsonify(link.to_dict())