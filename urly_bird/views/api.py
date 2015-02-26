import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import Links, User
from ..forms import LinkAddForm, LinkAddFormAPI, LinkUpdateForm
from ..extensions import login_manager, db


api = Blueprint("api", __name__)


def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


@login_manager.request_loader
def authorize_user(request):
    # Authorization: Basic username:password
    api_key = request.headers.get('Authorization')
    print('******************')
    print("\n\n\n\n\n", api_key, "\n\n\n")
    print('******************')
    if api_key:
       api_key = api_key.replace('Basic ', '', 1)
       api_key = api_key.split(":")
       email, password = api_key[0],  api_key[1]
       #api_key = base64.b64decode(api_key).decode("utf-8")
       #email, password = api_key.split(":")
       user = User.query.filter_by(email=email).first()
       if user.check_password(password):
            return user

    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        print('******************')
        print("\n\n\n\n\n", api_key, "\n\n\n")
        print('******************')
        return(user.id)
    else:
        #abort(401)
        return None


@api.route("/links", methods=["GET", "POST"])
def links():
    print('comes into links')
    if request.method == "POST":
        return create_link()


    links = Links.query.all()
    links = [link.to_dict() for link in links]
    return jsonify({"links": links})


def create_link():
    """Creates a new link from a JSON request."""
    user_id=require_authorization()
    print('************')
    print(user_id)
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = LinkAddForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        link = Links(title=form.title.data,
                     description=form.description.data,
                     long=form.long.data,
                     )
        last_id = db.session.query(db.func.max(Links.id)).scalar()
        link.set_short(last_id+1)
        link.user = user_id
        flash(link)
        db.session.add(link)
        db.session.commit()
        return (json.dumps(link.to_dict()), 201, {"Location": url_for(".link", id=link.id)})
    else:
        return json_response(400, form.errors)




@api.route("/links/<int:id>")
def link(id):
    link = Links.query.get_or_404(id)
    return jsonify(link.to_dict())
