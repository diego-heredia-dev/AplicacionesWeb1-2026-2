from urllib.parse import urlencode, urljoin, urlparse

from flask import (
    Blueprint,
    current_app,
    redirect,
    request,
    session,
    url_for,
)

from .oauth import oauth
from .tokens import verify_decode_jwt

bp = Blueprint("auth", __name__)


def safe_local_next(value):
    default = url_for("restaurantes.listar_restaurantes")

    if not value:
        return default

    target = urljoin(request.host_url, value)
    base = urlparse(request.host_url)
    parsed = urlparse(target)

    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        return default

    return parsed.path or default


@bp.route("/login")
def login():
    session["login_next"] = safe_local_next(request.args.get("next"))

    return oauth.auth0.authorize_redirect(
        url_for("auth.callback", _external=True),
        audience=current_app.config["AUTH0_AUDIENCE"],
    )


@bp.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    access_token = token.get("access_token")

    if not access_token:
        return "Auth0 no devolvió un access token.", 401

    try:
        claims = verify_decode_jwt(access_token)
    except Exception:
        session.clear()
        return "No se pudo validar el token de Auth0.", 401

    destination = safe_local_next(session.get("login_next"))
    session.clear()

    session["access_token"] = access_token
    session["user"] = {
        "sub": claims["sub"],
        "permissions": claims.get("permissions", []),
        "email": claims.get("email"),
        "name": claims.get("name"),
    }

    return redirect(destination)


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    params = urlencode({
        "client_id": current_app.config["AUTH0_CLIENT_ID"],
        "returnTo": url_for(
            "restaurantes.listar_restaurantes",
            _external=True,
        ),
    })

    domain = current_app.config["AUTH0_DOMAIN"]
    return redirect(f"https://{domain}/v2/logout?{params}")
