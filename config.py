import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


database_url = os.getenv(
    "DATABASE_URL"
)


if database_url:

    if database_url.startswith(
        "postgresql://"
    ):

        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    elif database_url.startswith(
        "postgres://"
    ):

        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )

else:

    database_url = "sqlite:///boda.db"


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave_temporal_desarrollo"
    )

    SQLALCHEMY_DATABASE_URI = (
        database_url
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }