"""Tests de DatabaseManager: esquema y migración idempotente de 'label'."""

import sqlite3

from models.database_manager import DatabaseManager


def _columns(conn, table):
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def test_initialize_crea_tablas_y_columna_label(db):
    conn = db._get_connection()
    tablas = {
        r["name"]
        for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    assert {"patients", "patient_media", "exercise_metrics"} <= tablas
    assert "label" in _columns(conn, "patient_media")


def test_migracion_agrega_label_a_bd_antigua(app_root):
    """Simula una BD v1 (sin columna label) y verifica que se migra."""
    manager = DatabaseManager()
    # Crea la tabla vieja SIN 'label', como en versiones previas
    conn = manager._get_connection()
    conn.execute(
        """
        CREATE TABLE patient_media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    assert "label" not in _columns(conn, "patient_media")

    # initialize_database debe migrar sin borrar datos
    manager.initialize_database()
    assert "label" in _columns(conn, "patient_media")

    # Idempotente: correr de nuevo no falla
    manager.initialize_database()
    manager.close()


def test_column_exists_helper(db):
    conn = db._get_connection()
    assert db._column_exists(conn, "patient_media", "file_name") is True
    assert db._column_exists(conn, "patient_media", "no_existe") is False
