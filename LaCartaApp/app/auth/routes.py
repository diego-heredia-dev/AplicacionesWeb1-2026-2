from flask import Blueprint, redirect, url_for, session, current_app, abort
from urllib.parse import urlencode

from .oauth import auth0

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login")
def login():
    redirect_uri = url_for("auth.callback", _external=True)

    return auth0().authorize_redirect(redirect_uri)

@bp.route("/callback")
def callback():
    token = auth0().authorize_access_token()

    userinfo = token.get("userinfo")

    if not userinfo or not userinfo.get("sub"):
        session.clear()
        abort(401)

    session["user"] = userinfo
    session["access_token"] = token["access_token"]

    return redirect(url_for("lacarta.listar_restaurantes"))

@bp.route("/logout")
def logout():
    session.clear()

    params = {
        "client_id": current_app.config["AUTH0_CLIENT_ID"],
        "returnTo": url_for("lacarta.listar_restaurantes", _external=True)
    }

    logout_url = (
        f"https://{current_app.config['AUTH0_DOMAIN']}/v2/logout?"
        f"{urlencode(params)}"
    )

    return redirect(logout_url)