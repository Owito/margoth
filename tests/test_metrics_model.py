"""Tests de MetricsModel: agregación de exercise_metrics."""

from models.metrics_model import MetricsModel
from models.semantic_exercise_model import SemanticExerciseModel


def _seed(db, patient_model, resultados):
    """resultados: lista de (is_correct, reaction_ms)."""
    p = patient_model.create_patient("Ana", "García")
    sem = SemanticExerciseModel(db, patient_model)
    for correcto, ms in resultados:
        sem.save_metric(p["id"], correcto, ms)
    return p


def test_summary_sin_datos(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    s = MetricsModel(db).get_patient_summary(p["id"])
    assert s["total"] == 0
    assert s["accuracy"] == 0.0
    assert s["tiempo_promedio_ms"] is None
    assert s["mejor_tiempo_ms"] is None


def test_summary_calcula_accuracy_y_tiempos(db, patient_model):
    p = _seed(db, patient_model, [(True, 1000.0), (False, 2000.0), (True, 3000.0)])
    s = MetricsModel(db).get_patient_summary(p["id"])
    assert s["total"] == 3
    assert s["correctos"] == 2
    assert s["incorrectos"] == 1
    assert abs(s["accuracy"] - (2 / 3 * 100)) < 0.001
    assert abs(s["tiempo_promedio_ms"] - 2000.0) < 0.001
    assert s["mejor_tiempo_ms"] == 1000.0


def test_summary_aislado_por_paciente(db, patient_model):
    p1 = _seed(db, patient_model, [(True, 500.0)])
    p2 = _seed(db, patient_model, [(False, 900.0), (False, 800.0)])
    m = MetricsModel(db)
    assert m.get_patient_summary(p1["id"])["total"] == 1
    assert m.get_patient_summary(p2["id"])["total"] == 2
    assert m.get_patient_summary(p2["id"])["correctos"] == 0


def test_recent_attempts_respeta_limite(db, patient_model):
    p = _seed(db, patient_model, [(True, float(i)) for i in range(30)])
    recientes = MetricsModel(db).get_recent_attempts(p["id"], limit=5)
    assert len(recientes) == 5
    assert all("reaction_time_ms" in r for r in recientes)


def test_daily_accuracy_agrupa(db, patient_model):
    p = _seed(db, patient_model, [(True, 100.0), (False, 200.0)])
    dias = MetricsModel(db).get_daily_accuracy(p["id"])
    # Todo en el mismo día (mismo tick) -> una fila con 2 intentos
    assert len(dias) == 1
    assert dias[0]["total"] == 2
    assert dias[0]["correctos"] == 1
    assert abs(dias[0]["accuracy"] - 50.0) < 0.001
