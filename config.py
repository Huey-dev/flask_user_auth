import os
import secrets

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class Config:
    # A generated fallback lets the app start before .env is configured. Set SECRET_KEY
    # in .env so flash messages remain valid across application restarts.
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "flask_user_auth")


def get_db_connection():
    """Open a connection using the database settings from the environment."""
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
    )
