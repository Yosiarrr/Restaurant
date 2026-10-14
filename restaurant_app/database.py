import sqlite3
from contextlib import closing
from pathlib import Path

from .config import DB_PATH


class RestaurantDatabase:
    """Class untuk menangani operasi database SQLite lokal maupun basis data eksternal."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(DB_PATH)

    def get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        schema_path = Path(__file__).resolve().parent.parent / "database_schema.sql"
        with self.get_connection() as connection:
            with closing(connection.cursor()) as cursor:
                sql = schema_path.read_text(encoding="utf-8")
                cursor.executescript(sql)
            connection.commit()

    def execute_query(self, query: str, params: tuple = (), fetchall: bool = False):
        with self.get_connection() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, params)
                if fetchall:
                    return cursor.fetchall()
                return cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()):
        with self.get_connection() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        with self.get_connection() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
