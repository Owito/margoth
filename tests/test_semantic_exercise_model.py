"""Tests de SemanticExerciseModel: métricas y generación de estímulos."""

from models.semantic_exercise_model import SemanticExerciseModel


def _model(db, patient_model):
    return SemanticExerciseModel(db, patient_model)


def test_save_metric_persiste_fila(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = _model(db, patient_model)

    ok = model.save_metric(p["id"], is_correct=True, reaction_time_ms=1234.5)
    assert ok is True

    conn = db._get_connection()
    row = conn.execute(
        "SELECT patient_id, exercise_type, is_correct, reaction_time_ms "
        "FROM exercise_metrics WHERE patient_id = ?",
        (p["id"],),
    ).fetchone()
    assert row["patient_id"] == p["id"]
    assert row["exercise_type"] == "semantic"
    assert row["is_correct"] == 1
    assert abs(row["reaction_time_ms"] - 1234.5) < 0.001


def test_save_metric_incorrecto_guarda_cero(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = _model(db, patient_model)
    model.save_metric(p["id"], is_correct=False, reaction_time_ms=10.0)
    conn = db._get_connection()
    row = conn.execute(
        "SELECT is_correct FROM exercise_metrics WHERE patient_id = ?", (p["id"],)
    ).fetchone()
    assert row["is_correct"] == 0


def test_get_next_stimulus_sin_imagenes_devuelve_none(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = _model(db, patient_model)
    assert model.get_next_stimulus(p["id"]) is None


def test_get_next_stimulus_construye_opciones(db, patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    # Tres imágenes -> 1 correcta + 2 distractores
    for nombre in ("perro.png", "gato.png", "casa.png"):
        patient_model.import_media(p["id"], make_image(nombre))

    model = _model(db, patient_model)
    stim = model.get_next_stimulus(p["id"])

    assert stim is not None
    assert stim["image_bytes"]  # bytes de la imagen leídos
    assert stim["correct_answer"] in stim["options"]
    assert len(stim["options"]) == 3
    assert len(set(stim["options"])) == 3  # sin duplicados


def test_get_next_stimulus_usa_label_no_nombre_de_archivo(db, patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("IMG_0001.png"), label="Manzana")
    model = _model(db, patient_model)
    stim = model.get_next_stimulus(p["id"])
    assert stim["correct_answer"] == "Manzana"
    assert "IMG_0001" not in stim["options"]


def test_get_next_stimulus_una_sola_imagen_rellena_distractores(db, patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("solo.png"))
    model = _model(db, patient_model)
    stim = model.get_next_stimulus(p["id"])
    assert stim is not None
    assert len(stim["options"]) == 3
    assert stim["correct_answer"] in stim["options"]
