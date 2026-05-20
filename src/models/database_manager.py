import sqlite3
import os


class DatabaseManager:
    """Gestiona la conexión y el esquema de la base de datos SQLite local."""

    def __init__(self, db_filename="margoth.db"):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._data_dir = os.path.join(project_root, "data")
        self._media_dir = os.path.join(project_root, "media")
        self._db_path = os.path.join(self._data_dir, db_filename)
        self._connection = None

        os.makedirs(self._data_dir, exist_ok=True)
        os.makedirs(self._media_dir, exist_ok=True)

    @property
    def media_dir(self):
        return self._media_dir

    def _get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def initialize_database(self):
        conn = self._get_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date DATE,
                notes TEXT,
                media_folder TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
