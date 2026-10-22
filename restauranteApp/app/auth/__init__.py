from functools import wraps

from flask import redirect, request, session, url_for
from jwt.exceptions import PyJWTError

from .errors import AuthError
from .tokens import verify_decode_jwt


def current_user():
    token = session.get("access_token")

    if not token:
        return None

    try:
        claims = verify_decode_jwt(token)
    except (PyJWTError, ValueError):
        session.clear()
        return None

    return {
        "sub": claims["sub"],
        "permissions": claims.get("permissions", []),
        "email": claims.get("email"),
        "name": claims.get("name"),
    }


def requires_auth(permission=None):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()

            if user is None:
                return redirect(
                    url_for("auth.login", next=request.path)
                )

            if permission and permission not in user["permissions"]:
                raise AuthError(
                    "No tienes permiso para realizar esta acción.",
                    403,
                )

            return view(*args, **kwargs)

        return wrapped
    return decorator
