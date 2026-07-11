import json
import os
import uuid

from utils.path_resolver import PathResolver


class CAABoardModel:
    """Persistencia de tableros CAA como JSON en la carpeta del paciente.

    Un paciente puede tener varios tableros. Se guardan en
    ``media/{uuid}/caa_boards.json`` con la forma ``{"boards": [ ... ]}``.
    """

    def __init__(self, db_manager):
        self._db = db_manager

    # ── Lectura de bytes de medios ────────────────────────────────
    def load_audio_bytes(self, audio_path):
        if not audio_path or not os.path.isfile(audio_path):
            return None
        try:
            with open(audio_path, "rb") as handle:
                return handle.read()
        except OSError as exc:
            print(f"Error leyendo audio: {exc}")
            return None

    def _load_image_bytes(self, image_path):
        if not image_path or not os.path.isfile(image_path):
            return None
        try:
            with open(image_path, "rb") as handle:
                return handle.read()
        except OSError as exc:
            print(f"Error leyendo imagen: {exc}")
            return None

    # ── Rutas ─────────────────────────────────────────────────────
    def _media_path(self, patient_dict):
        media_folder = patient_dict.get("media_folder", "")
        app_root = PathResolver.get_app_data_path()
        return os.path.join(app_root, "media", media_folder)

    def _json_path(self, patient_dict):
        return os.path.join(self._media_path(patient_dict), "caa_boards.json")

    # ── Lectura/escritura del archivo completo ────────────────────
    def _read_all(self, patient_dict):
        json_path = self._json_path(patient_dict)
        if not os.path.isfile(json_path):
            return []
        try:
            with open(json_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data.get("boards", []) or []
        except (json.JSONDecodeError, OSError, KeyError) as exc:
            print(f"Error leyendo caa_boards.json: {exc}")
            return []

    def _write_all(self, patient_dict, boards):
        media_path = self._media_path(patient_dict)
        os.makedirs(media_path, exist_ok=True)
        try:
            with open(self._json_path(patient_dict), "w", encoding="utf-8") as handle:
                json.dump({"boards": boards}, handle, indent=2, ensure_ascii=False)
        except OSError as exc:
            print(f"Error guardando caa_boards.json: {exc}")
            return False
        return True

    # ── API pública ───────────────────────────────────────────────
    def list_boards(self, patient_dict):
        """Metadatos de los tableros (id, nombre, tamaño) sin cargar bytes."""
        boards = self._read_all(patient_dict)
        resultado = []
        for board in boards:
            resultado.append(
                {
                    "id": board.get("id", ""),
                    "name": board.get("name", "Tablero CAA"),
                    "grid_size": board.get("grid_size", {"rows": 2, "cols": 2}),
                }
            )
        return resultado

    def _hydrate(self, patient_dict, board):
        """Convierte un tablero crudo en (board, items con bytes de imagen)."""
        media_path = self._media_path(patient_dict)
        items = []
        for item in board.get("items", []):
            image_file = item.get("image_file", "")
            audio_file = item.get("audio_file", "")
            image_path = os.path.join(media_path, image_file) if image_file else ""
            audio_path = os.path.join(media_path, audio_file) if audio_file else ""
            items.append(
                {
                    "position": item.get("position", [0, 0]),
                    "label": item.get("label", ""),
                    "image_file": image_file,
                    "audio_file": audio_file,
                    "image_bytes": self._load_image_bytes(image_path),
                    "audio_path": audio_path,
                }
            )
        return board, items

    def load_board(self, patient_dict, board_id=None):
        """Carga un tablero por id; si no se indica, el primero disponible."""
        boards = self._read_all(patient_dict)
        if not boards:
            return {"name": "Tablero CAA", "items": []}, []

        board = None
        if board_id is not None:
            board = next((b for b in boards if b.get("id") == board_id), None)
        if board is None:
            board = boards[0]
        return self._hydrate(patient_dict, board)

    def load_first_board(self, patient_dict):
        """Compatibilidad: carga el primer tablero del paciente."""
        return self.load_board(patient_dict, board_id=None)

    def save_board(self, patient_dict, board_data):
        """Inserta o actualiza (upsert) un tablero por su id, sin borrar los demás."""
        if not board_data.get("id"):
            board_data = dict(board_data)
            board_data["id"] = f"board_{uuid.uuid4().hex[:8]}"

        boards = self._read_all(patient_dict)
        for idx, existing in enumerate(boards):
            if existing.get("id") == board_data["id"]:
                boards[idx] = board_data
                break
        else:
            boards.append(board_data)

        return self._write_all(patient_dict, boards)

    def delete_board(self, patient_dict, board_id):
        boards = self._read_all(patient_dict)
        nuevos = [b for b in boards if b.get("id") != board_id]
        if len(nuevos) == len(boards):
            return False
        return self._write_all(patient_dict, nuevos)

    def create_test_board(self, patient_dict):
        test_board = {
            "id": f"board_{uuid.uuid4().hex[:8]}",
            "name": "Tablero de Prueba",
            "grid_size": {"rows": 2, "cols": 2},
            "items": [
                {"position": [0, 0], "label": "Opcion 1", "image_file": "", "audio_file": ""},
                {"position": [0, 1], "label": "Opcion 2", "image_file": "", "audio_file": ""},
                {"position": [1, 0], "label": "Opcion 3", "image_file": "", "audio_file": ""},
                {"position": [1, 1], "label": "Opcion 4", "image_file": "", "audio_file": ""},
            ],
        }
        self.save_board(patient_dict, test_board)
