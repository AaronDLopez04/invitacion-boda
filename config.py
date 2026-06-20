import os

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave_temporal_desarrollo"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///boda.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False