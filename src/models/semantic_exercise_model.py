import os
import random
import sqlite3


class SemanticExerciseModel:
    def __init__(self, db_manager, patient_model):
        self._db = db_manager
        self._patient_model = patient_model

    def _get_media_path(self, patient_id):
        patient = self._patient_model.get_patient_by_id(patient_id)
        if not patient:
            return None
        media_folder = patient.get("media_folder", "")
        if not media_folder:
            return None
        return os.path.join(self._db.media_dir, media_folder)

    def get_next_stimulus(self, patient_id):
        media_path = self._get_media_path(patient_id)
        if not media_path:
            return None

        conn = self._db._get_connection()
        row = conn.execute(
            """
            SELECT file_name
            FROM patient_media
            WHERE patient_id = ? AND file_type = 'image'
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (patient_id,),
        ).fetchone()

        if not row:
            return None

        file_name = row["file_name"]
        image_path = os.path.join(media_path, file_name)
        if not os.path.isfile(image_path):
            return None

        try:
            with open(image_path, "rb") as handle:
                image_bytes = handle.read()
        except OSError as exc:
            print(f"Error leyendo imagen: {exc}")
            return None

        correct_answer = os.path.splitext(file_name)[0]

        false_options = []
        other_rows = conn.execute(
            """
            SELECT file_name
            FROM patient_media
            WHERE patient_id = ? AND file_type = 'image' AND file_name != ?
            ORDER BY RANDOM()
            LIMIT 2
            """,
            (patient_id, file_name),
        ).fetchall()

        for other in other_rows:
            false_options.append(os.path.splitext(other["file_name"])[0])

        while len(false_options) < 2:
            false_options.append(f"Opción Falsa {len(false_options) + 1}")

        options = [correct_answer] + false_options[:2]
        random.shuffle(options)

        return {
            "image_bytes": image_bytes,
            "correct_answer": correct_answer,
            "options": options,
        }

    def save_metric(self, patient_id, is_correct, reaction_time_ms):
        try:
            conn = self._db._get_connection()
            conn.execute(
                """
                INSERT INTO exercise_metrics (
                    patient_id, exercise_type, is_correct, reaction_time_ms
                ) VALUES (?, ?, ?, ?)
                """,
                (patient_id, "semantic", int(is_correct), reaction_time_ms),
            )
            conn.commit()
        except sqlite3.Error as exc:
            print(f"Error guardando metricas: {exc}")
            return False

        return True
