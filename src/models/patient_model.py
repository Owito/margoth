import uuid
import os
import shutil
import sqlite3


class PatientModel:
    """CRUD de pacientes. Genera carpetas de medios por UUID."""

    def __init__(self, db_manager):
        self._db = db_manager

        self._image_extensions = {".png", ".jpg", ".jpeg"}
        self._audio_extensions = {".mp3", ".wav"}

    def create_patient(self, first_name, last_name, birth_date=None, notes=None):
        media_folder = str(uuid.uuid4())
        folder_path = os.path.join(self._db.media_dir, media_folder)
        os.makedirs(folder_path, exist_ok=True)

        conn = self._db._get_connection()
        cursor = conn.execute(
            """
            INSERT INTO patients (first_name, last_name, birth_date, notes, media_folder)
            VALUES (?, ?, ?, ?, ?)
            """,
            (first_name, last_name, birth_date, notes, media_folder),
        )
        conn.commit()
        return self.get_patient_by_id(cursor.lastrowid)

    def get_all_patients(self):
        conn = self._db._get_connection()
        rows = conn.execute(
            "SELECT * FROM patients ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_patient_by_id(self, patient_id):
        conn = self._db._get_connection()
        row = conn.execute(
            "SELECT * FROM patients WHERE id = ?", (patient_id,)
        ).fetchone()
        return dict(row) if row else None

    def update_patient(self, patient_id, **kwargs):
        allowed = {"first_name", "last_name", "birth_date", "notes"}
        fields = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            return self.get_patient_by_id(patient_id)

        set_clause = ", ".join(f"{col} = ?" for col in fields)
        values = list(fields.values()) + [patient_id]

        conn = self._db._get_connection()
        conn.execute(
            f"UPDATE patients SET {set_clause} WHERE id = ?", values
        )
        conn.commit()
        return self.get_patient_by_id(patient_id)

    def import_media(self, patient_id, source_file_path):
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return None

        media_folder = patient.get("media_folder", "")
        if not media_folder:
            return None

        if not source_file_path or not os.path.isfile(source_file_path):
            return None

        file_type = self._get_file_type(source_file_path)
        if not file_type:
            return None

        dest_dir = os.path.join(self._db.media_dir, media_folder)
        os.makedirs(dest_dir, exist_ok=True)

        filename = os.path.basename(source_file_path)
        final_filename = self._unique_filename(dest_dir, filename)
        dest_path = os.path.join(dest_dir, final_filename)

        try:
            shutil.copy2(source_file_path, dest_path)
        except (OSError, shutil.Error) as exc:
            print(f"Error copiando archivo: {exc}")
            return None

        try:
            conn = self._db._get_connection()
            conn.execute(
                """
                INSERT INTO patient_media (patient_id, file_name, file_type)
                VALUES (?, ?, ?)
                """,
                (patient_id, final_filename, file_type),
            )
            conn.commit()
        except sqlite3.Error as exc:
            print(f"Error registrando medio en DB: {exc}")
            return None

        return final_filename

    def get_patient_media(self, patient_id, file_type=None):
        conn = self._db._get_connection()
        if file_type:
            rows = conn.execute(
                """
                SELECT * FROM patient_media
                WHERE patient_id = ? AND file_type = ?
                ORDER BY created_at DESC
                """,
                (patient_id, file_type),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM patient_media
                WHERE patient_id = ?
                ORDER BY created_at DESC
                """,
                (patient_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def _get_file_type(self, source_file_path):
        ext = os.path.splitext(source_file_path)[1].lower()
        if ext in self._image_extensions:
            return "image"
        if ext in self._audio_extensions:
            return "audio"
        return None

    def _unique_filename(self, dest_dir, filename):
        base, ext = os.path.splitext(filename)
        dest_path = os.path.join(dest_dir, filename)
        if not os.path.exists(dest_path):
            return filename

        suffix = str(uuid.uuid4())[:6]
        return f"{base}_{suffix}{ext}"
