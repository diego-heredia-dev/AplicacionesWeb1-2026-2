from flask import Blueprint, redirect, url_for, session

from .oauth import auth0

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login")
def login():
    redirect_uri = url_for("auth.callback", _external=True)

    return auth0().authorize_redirect(redirect_uri)


@bp.route("/callback")
def callback():
    token = auth0().authorize_access_token()

    session["user"] = token.get("userinfo")
    session["access_token"] = token["access_token"]

    return redirect(url_for("lacarta.listar_restaurantes"))