import uuid
import os


class PatientModel:
    """CRUD de pacientes. Genera carpetas de medios por UUID."""

    def __init__(self, db_manager):
        self._db = db_manager

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
