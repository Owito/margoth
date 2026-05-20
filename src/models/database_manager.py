import sqlite3
import os
from utils.path_resolver import PathResolver


class DatabaseManager:
    """Gestiona la conexión y el esquema de la base de datos SQLite local."""

    def __init__(self, db_filename="margoth.db"):
        app_root = PathResolver.get_app_data_path()
        self._data_dir = os.path.join(app_root, "data")
        self._media_dir = os.path.join(app_root, "media")
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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS patient_media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercise_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                exercise_type TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL,
                reaction_time_ms REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
            """
        )
        conn.commit()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
