import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth0
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "").strip()
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "").strip()
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
    AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "").strip()

    # Seguridad de la sesión
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
    )

    # Proxy inverso (Nginx en producción)
    BEHIND_PROXY = os.environ.get("BEHIND_PROXY", "0") == "1"
