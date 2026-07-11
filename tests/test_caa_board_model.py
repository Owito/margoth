"""Tests de CAABoardModel: round-trip de tableros y estado vacío."""

import json
import os

from models.caa_board_model import CAABoardModel


def _board():
    return {
        "id": "board_01",
        "name": "Rutina mañana",
        "grid_size": {"rows": 2, "cols": 2},
        "items": [
            {"position": [0, 0], "label": "Agua", "image_file": "agua.png", "audio_file": "agua.wav"},
            {"position": [0, 1], "label": "", "image_file": "", "audio_file": ""},
        ],
    }


def test_load_first_board_sin_json_devuelve_vacio(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    board, items = model.load_first_board(p)
    assert items == []
    assert "name" in board


def test_save_y_load_board_roundtrip(db, patient_model, make_image):
    p = patient_model.create_patient("Ana", "García")
    # La imagen referenciada debe existir para que se carguen sus bytes
    patient_model.import_media(p["id"], make_image("agua.png"))

    model = CAABoardModel(db)
    assert model.save_board(p, _board()) is True

    board, items = model.load_first_board(p)
    assert board["name"] == "Rutina mañana"
    assert len(items) == 2
    primera = items[0]
    assert primera["label"] == "Agua"
    assert primera["position"] == [0, 0]
    assert primera["image_bytes"]  # bytes cargados de la imagen real
    assert primera["audio_path"].endswith("agua.wav")


def test_save_board_escribe_json_en_carpeta_paciente(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.save_board(p, _board())
    json_path = os.path.join(db.media_dir, p["media_folder"], "caa_boards.json")
    assert os.path.isfile(json_path)
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)
    assert data["boards"][0]["name"] == "Rutina mañana"


def test_create_test_board_genera_grilla_2x2(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.create_test_board(p)
    board, items = model.load_first_board(p)
    assert len(items) == 4


def test_save_board_upsert_no_borra_otros(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    b1 = {"id": "b1", "name": "Casa", "grid_size": {"rows": 2, "cols": 2}, "items": []}
    b2 = {"id": "b2", "name": "Comida", "grid_size": {"rows": 3, "cols": 3}, "items": []}
    model.save_board(p, b1)
    model.save_board(p, b2)  # NO debe sobrescribir b1

    tableros = model.list_boards(p)
    assert len(tableros) == 2
    ids = {t["id"] for t in tableros}
    assert ids == {"b1", "b2"}


def test_save_board_actualiza_existente_por_id(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.save_board(p, {"id": "b1", "name": "Viejo", "items": []})
    model.save_board(p, {"id": "b1", "name": "Nuevo", "items": []})
    tableros = model.list_boards(p)
    assert len(tableros) == 1
    assert tableros[0]["name"] == "Nuevo"


def test_save_board_sin_id_genera_uno(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.save_board(p, {"name": "Sin id", "items": []})
    tableros = model.list_boards(p)
    assert len(tableros) == 1
    assert tableros[0]["id"]  # id generado no vacío


def test_load_board_por_id(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.save_board(p, {"id": "b1", "name": "Uno", "grid_size": {"rows": 2, "cols": 2}, "items": []})
    model.save_board(p, {"id": "b2", "name": "Dos", "grid_size": {"rows": 2, "cols": 2}, "items": []})
    board, _ = model.load_board(p, "b2")
    assert board["name"] == "Dos"


def test_delete_board(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    model = CAABoardModel(db)
    model.save_board(p, {"id": "b1", "name": "Uno", "items": []})
    model.save_board(p, {"id": "b2", "name": "Dos", "items": []})
    assert model.delete_board(p, "b1") is True
    assert {t["id"] for t in model.list_boards(p)} == {"b2"}
    assert model.delete_board(p, "inexistente") is False


def test_load_first_board_json_corrupto_no_lanza(db, patient_model):
    p = patient_model.create_patient("Ana", "García")
    folder = os.path.join(db.media_dir, p["media_folder"])
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "caa_boards.json"), "w", encoding="utf-8") as fh:
        fh.write("{ esto no es json valido ")
    model = CAABoardModel(db)
    board, items = model.load_first_board(p)  # no debe lanzar
    assert items == []
