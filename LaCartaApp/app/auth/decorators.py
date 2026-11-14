from functools import wraps

import jwt
from jwt import PyJWKClient

from flask import current_app, session, redirect, url_for, abort, g


def get_permissions():
    if hasattr(g, "auth0_permissions"):
        return g.auth0_permissions

    permissions = set()
    access_token = session.get("access_token")

    if access_token:
        try:
            domain = current_app.config["AUTH0_DOMAIN"]
            audience = current_app.config["AUTH0_AUDIENCE"]

            issuer = f"https://{domain}/"

            jwks_client = PyJWKClient(f"{issuer}.well-known/jwks.json")
            signing_key = jwks_client.get_signing_key_from_jwt(access_token)

            payload = jwt.decode(
                access_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=audience,
                issuer=issuer
            )

            permissions = set(payload.get("permissions", []))

        except jwt.InvalidTokenError:
            session.clear()

    g.auth0_permissions = permissions

    return permissions


def has_permission(permission):
    return permission in get_permissions()


def requires_auth(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("access_token"):
                return redirect(url_for("auth.login"))

            permissions = get_permissions()

            if not session.get("access_token"):
                return redirect(url_for("auth.login"))

            if permission not in permissions:
                abort(403)

            return func(*args, **kwargs)

        return wrapper
    return decorator