"""Agregación de métricas clínicas a partir de exercise_metrics.

Solo lectura: no toca UI. Provee el resumen de progreso por paciente que
consume la vista de reportes.
"""


class MetricsModel:
    def __init__(self, db_manager):
        self._db = db_manager

    def get_patient_summary(self, patient_id):
        """Devuelve un resumen agregado de todos los intentos del paciente."""
        conn = self._db._get_connection()
        row = conn.execute(
            """
            SELECT
                COUNT(*)                         AS total,
                COALESCE(SUM(is_correct), 0)     AS correctos,
                AVG(reaction_time_ms)            AS tiempo_promedio,
                MIN(reaction_time_ms)            AS mejor_tiempo,
                MAX(created_at)                  AS ultima_actividad
            FROM exercise_metrics
            WHERE patient_id = ?
            """,
            (patient_id,),
        ).fetchone()

        total = row["total"] or 0
        correctos = row["correctos"] or 0
        accuracy = (correctos / total * 100.0) if total else 0.0

        return {
            "total": total,
            "correctos": correctos,
            "incorrectos": total - correctos,
            "accuracy": accuracy,
            "tiempo_promedio_ms": row["tiempo_promedio"] if total else None,
            "mejor_tiempo_ms": row["mejor_tiempo"] if total else None,
            "ultima_actividad": row["ultima_actividad"],
        }

    def get_recent_attempts(self, patient_id, limit=20):
        """Últimos intentos (más recientes primero)."""
        conn = self._db._get_connection()
        rows = conn.execute(
            """
            SELECT is_correct, reaction_time_ms, created_at
            FROM exercise_metrics
            WHERE patient_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (patient_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_daily_accuracy(self, patient_id, limit_days=14):
        """Precisión por día (para ver tendencia). Más reciente primero."""
        conn = self._db._get_connection()
        rows = conn.execute(
            """
            SELECT
                DATE(created_at)             AS dia,
                COUNT(*)                     AS total,
                COALESCE(SUM(is_correct), 0) AS correctos,
                AVG(reaction_time_ms)        AS tiempo_promedio
            FROM exercise_metrics
            WHERE patient_id = ?
            GROUP BY DATE(created_at)
            ORDER BY dia DESC
            LIMIT ?
            """,
            (patient_id, limit_days),
        ).fetchall()
        resultado = []
        for r in rows:
            total = r["total"] or 0
            correctos = r["correctos"] or 0
            resultado.append(
                {
                    "dia": r["dia"],
                    "total": total,
                    "correctos": correctos,
                    "accuracy": (correctos / total * 100.0) if total else 0.0,
                    "tiempo_promedio_ms": r["tiempo_promedio"],
                }
            )
        return resultado
