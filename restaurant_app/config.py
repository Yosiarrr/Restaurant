import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "restaurant_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PATH = BASE_DIR / "restaurant.db"


def get_database_url() -> str:
    if DB_TYPE == "mysql":
        return (
            f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    return f"sqlite:///{DB_PATH}"
