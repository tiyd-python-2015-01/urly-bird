import base64
import json
from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import User, URL
from ..forms import URLForm
from ..extensions import login_manager, db

api = Blueprint("api", __name__)


def json_response(code, data):
    return json.dumps(data), code, {"Content-Type": "application/json"}


@api.app_errorhandler(401)
def unauthorized(request):
    return "", 401, {"Content-Type": "application/json"}


@login_manager.request_loader
def authorize_user(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        api_key = base64.b64decode(api_key).decode("utf-8")
        email, password = api_key(":")

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user
    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
    else:
        abort(401)


@api.route("/urls", methods=['GET', 'POST'])
def urls():
    if request.method == "POST":
        return create_url()
    all_urls = URL.query.all()
    all_urls = [url.to_dict() for url in all_urls]
    return jsonify({"urls": all_urls})


def create_url():
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = URLForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():

        new_url = URL.query.filter_by(long_address=form.address.data).first()
        if new_url:
            return json_response(400,{"url": "This url has been taken"})
        else:
            new_url = URL(**form.data)
            db.session.add(new_url)
            db.session.commit()
            return json.dumps(urls.to_dict()), 201, {"Location": url_for(".url", id=new_url.id)}
    else:
        return json_response(400, form.errors)


@api.route("/urls/<int:url_id>")
def url(url_id):
    request_url = URL.query.get_or_404(url_id)
    return jsonify(request_url.to_dict())
