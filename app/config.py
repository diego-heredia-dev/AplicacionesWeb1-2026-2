import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "asdavgewa23",
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://lacarta:lewebivuavo@localhost:5432/lacarta",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False