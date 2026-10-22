from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_auth0(app):
    oauth.init_app(app)

    oauth.register(
        name="auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        server_metadata_url=(
            f"https://{app.config['AUTH0_DOMAIN']}/"
            ".well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": "openid profile email",
        },
    )
