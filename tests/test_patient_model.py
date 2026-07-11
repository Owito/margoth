"""Tests de PatientModel: CRUD, importación de medios y utilidades."""

import os


def test_create_patient_devuelve_registro_con_carpeta(patient_model, db):
    p = patient_model.create_patient("Ana", "García", "1950-05-01", "notas")

    assert p["id"] > 0
    assert p["first_name"] == "Ana"
    assert p["last_name"] == "García"
    assert p["media_folder"]  # UUID no vacío
    # La carpeta de medios se crea físicamente
    assert os.path.isdir(os.path.join(db.media_dir, p["media_folder"]))


def test_media_folder_es_unico_por_paciente(patient_model):
    a = patient_model.create_patient("Ana", "Uno")
    b = patient_model.create_patient("Ben", "Dos")
    assert a["media_folder"] != b["media_folder"]


def test_get_all_patients_ordena_por_mas_reciente(patient_model):
    patient_model.create_patient("Uno", "A")
    patient_model.create_patient("Dos", "B")
    todos = patient_model.get_all_patients()
    assert len(todos) == 2
    # created_at DESC: el último creado va primero (o empatan en el mismo tick)
    ids = [p["id"] for p in todos]
    assert set(ids) == {1, 2}


def test_get_patient_by_id_inexistente_devuelve_none(patient_model):
    assert patient_model.get_patient_by_id(999) is None


def test_update_patient_modifica_campos_permitidos(patient_model):
    p = patient_model.create_patient("Ana", "García", notes="vieja")
    actualizado = patient_model.update_patient(p["id"], first_name="Ana María", notes="nueva")
    assert actualizado["first_name"] == "Ana María"
    assert actualizado["notes"] == "nueva"


def test_update_patient_ignora_campos_no_permitidos(patient_model):
    p = patient_model.create_patient("Ana", "García")
    original_folder = p["media_folder"]
    actualizado = patient_model.update_patient(p["id"], media_folder="hackeado", id=42)
    assert actualizado["media_folder"] == original_folder
    assert actualizado["id"] == p["id"]


def test_import_media_imagen(patient_model, db, make_image):
    p = patient_model.create_patient("Ana", "García")
    src = make_image("gato.png")

    nombre = patient_model.import_media(p["id"], src)

    assert nombre == "gato.png"
    # Copiado físicamente a la carpeta del paciente
    dest = os.path.join(db.media_dir, p["media_folder"], "gato.png")
    assert os.path.isfile(dest)
    # Registrado en la BD como 'image'
    medios = patient_model.get_patient_media(p["id"], "image")
    assert len(medios) == 1
    assert medios[0]["file_type"] == "image"


def test_import_media_audio(patient_model, db, make_audio):
    p = patient_model.create_patient("Ana", "García")
    nombre = patient_model.import_media(p["id"], make_audio("hola.wav"))
    assert nombre == "hola.wav"
    medios = patient_model.get_patient_media(p["id"], "audio")
    assert len(medios) == 1 and medios[0]["file_type"] == "audio"


def test_import_media_tipo_no_soportado(patient_model, tmp_path):
    p = patient_model.create_patient("Ana", "García")
    txt = tmp_path / "notas.txt"
    txt.write_text("hola")
    assert patient_model.import_media(p["id"], str(txt)) is None


def test_import_media_archivo_inexistente(patient_model):
    p = patient_model.create_patient("Ana", "García")
    assert patient_model.import_media(p["id"], "no_existe.png") is None


def test_import_media_paciente_inexistente(patient_model, make_image):
    src = make_image()
    assert patient_model.import_media(999, src) is None


def test_import_media_nombre_duplicado_no_sobrescribe(patient_model, db, make_image):
    p = patient_model.create_patient("Ana", "García")
    n1 = patient_model.import_media(p["id"], make_image("dup.png"))
    n2 = patient_model.import_media(p["id"], make_image("dup.png"))
    assert n1 == "dup.png"
    assert n2 != n1  # segundo recibe sufijo único
    assert n2.startswith("dup_") and n2.endswith(".png")
    # Ambos archivos existen
    folder = os.path.join(db.media_dir, p["media_folder"])
    assert os.path.isfile(os.path.join(folder, n1))
    assert os.path.isfile(os.path.join(folder, n2))


def test_get_patient_media_filtra_por_tipo(patient_model, make_image, make_audio):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("i.png"))
    patient_model.import_media(p["id"], make_audio("a.wav"))

    solo_img = patient_model.get_patient_media(p["id"], "image")
    solo_aud = patient_model.get_patient_media(p["id"], "audio")
    todos = patient_model.get_patient_media(p["id"])

    assert len(solo_img) == 1 and solo_img[0]["file_type"] == "image"
    assert len(solo_aud) == 1 and solo_aud[0]["file_type"] == "audio"
    assert len(todos) == 2


def test_import_media_guarda_label_explicita(patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("IMG_9921.png"), label="Perro")
    medio = patient_model.get_patient_media(p["id"], "image")[0]
    assert medio["label"] == "Perro"


def test_import_media_label_por_defecto_es_nombre_sin_extension(patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("gato.png"))
    medio = patient_model.get_patient_media(p["id"], "image")[0]
    assert medio["label"] == "gato"


def test_import_media_label_vacia_cae_al_nombre(patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    patient_model.import_media(p["id"], make_image("casa.png"), label="   ")
    medio = patient_model.get_patient_media(p["id"], "image")[0]
    assert medio["label"] == "casa"


def test_get_file_type_extensiones(patient_model):
    assert patient_model._get_file_type("x.PNG") == "image"
    assert patient_model._get_file_type("x.jpeg") == "image"
    assert patient_model._get_file_type("x.MP3") == "audio"
    assert patient_model._get_file_type("x.wav") == "audio"
    assert patient_model._get_file_type("x.txt") is None
