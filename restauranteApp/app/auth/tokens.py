import jwt
from flask import current_app
from jwt import PyJWKClient


def jwks_client(domain):
    return PyJWKClient(
        f"https://{domain}/.well-known/jwks.json"
    )


def verify_decode_jwt(token):
    domain = current_app.config["AUTH0_DOMAIN"]
    audience = current_app.config["AUTH0_AUDIENCE"]

    if not domain or not audience:
        raise ValueError(
            "La configuración de Auth0 está incompleta."
        )

    client = current_app.extensions.get("auth0_jwks")

    if client is None:
        raise ValueError(
            "El cliente JWKS de Auth0 no está configurado."
        )

    signing_key = client.get_signing_key_from_jwt(token)

    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=audience,
        issuer=f"https://{domain}/",
    )
