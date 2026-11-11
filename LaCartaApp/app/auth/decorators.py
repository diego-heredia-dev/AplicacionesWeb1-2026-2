from functools import wraps

import jwt
from jwt import PyJWKClient

from flask import current_app, session, redirect, url_for, abort


def requires_auth(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # 1. Comprobar si existe una sesión
            access_token = session.get("access_token")

            if not access_token:
                return redirect(url_for("auth.login"))

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

                permissions = payload.get("permissions", [])

                if permission not in permissions:
                    abort(403)

                return func(*args, **kwargs)

            except jwt.InvalidTokenError:
                session.clear()
                return redirect(url_for("auth.login"))

        return wrapper
    return decorator