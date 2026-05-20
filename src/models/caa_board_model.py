import json
import os


class CAABoardModel:
    def __init__(self, db_manager):
        self._db = db_manager

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

    def _media_path(self, patient_dict):
        media_folder = patient_dict.get("media_folder", "")
        return os.path.join(self._db.media_dir, media_folder)

    def load_first_board(self, patient_dict):
        media_path = self._media_path(patient_dict)
        json_path = os.path.join(media_path, "caa_boards.json")

        if not os.path.isfile(json_path):
            return {"name": "Tablero CAA", "items": []}, []

        try:
            with open(json_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            boards = data.get("boards", [])
            if boards:
                board = boards[0]
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
                            "image_bytes": self._load_image_bytes(image_path),
                            "audio_path": audio_path,
                        }
                    )
                return board, items
            return {"name": "Tableros vacios", "items": []}, []
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"Error leyendo caa_boards.json: {exc}")
            return {"name": "Error en tablero", "items": []}, []

    def create_test_board(self, patient_dict):
        media_path = self._media_path(patient_dict)
        os.makedirs(media_path, exist_ok=True)
        json_path = os.path.join(media_path, "caa_boards.json")

        test_board = {
            "boards": [
                {
                    "id": "test_01",
                    "name": "Tablero de Prueba",
                    "grid_size": {"rows": 2, "cols": 2},
                    "items": [
                        {
                            "position": [0, 0],
                            "label": "Opcion 1",
                            "image_file": "",
                            "audio_file": "",
                        },
                        {
                            "position": [0, 1],
                            "label": "Opcion 2",
                            "image_file": "",
                            "audio_file": "",
                        },
                        {
                            "position": [1, 0],
                            "label": "Opcion 3",
                            "image_file": "",
                            "audio_file": "",
                        },
                        {
                            "position": [1, 1],
                            "label": "Opcion 4",
                            "image_file": "",
                            "audio_file": "",
                        },
                    ],
                }
            ]
        }

        try:
            with open(json_path, "w", encoding="utf-8") as handle:
                json.dump(test_board, handle, indent=2, ensure_ascii=False)
        except OSError as exc:
            print(f"Error creando tablero de prueba: {exc}")
