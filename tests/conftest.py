"""Configuración compartida de pytest.

Aísla la capa de datos en un directorio temporal por test, sin tocar la
carpeta real ``data/`` ni ``media/`` del proyecto. No importa PyQt6: los
tests de ``models/`` corren headless.
"""

import os
import sys

import pytest

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from utils.path_resolver import PathResolver  # noqa: E402
from models.database_manager import DatabaseManager  # noqa: E402
from models.patient_model import PatientModel  # noqa: E402


@pytest.fixture
def app_root(tmp_path, monkeypatch):
    """Redirige la raíz de datos de la app al tmp_path del test."""
    root = str(tmp_path)
    monkeypatch.setattr(PathResolver, "get_app_data_path", staticmethod(lambda: root))
    return tmp_path


@pytest.fixture
def db(app_root):
    manager = DatabaseManager()
    manager.initialize_database()
    yield manager
    manager.close()


@pytest.fixture
def patient_model(db):
    return PatientModel(db)


@pytest.fixture
def make_image(tmp_path):
    """Crea un PNG mínimo válido y devuelve su ruta."""
    from PIL import Image

    counter = {"n": 0}

    def _make(name="foto.png", size=(8, 8), color=(120, 200, 90)):
        counter["n"] += 1
        # Subcarpeta única para preservar el basename exacto solicitado
        sub = tmp_path / "src_img" / str(counter["n"])
        sub.mkdir(parents=True, exist_ok=True)
        path = sub / name
        Image.new("RGB", size, color).save(path)
        return str(path)

    return _make


@pytest.fixture
def make_audio(tmp_path):
    """Crea un archivo .wav mínimo (cabecera RIFF) y devuelve su ruta."""
    import struct
    import wave

    counter = {"n": 0}

    def _make(name="sonido.wav"):
        counter["n"] += 1
        sub = tmp_path / "src_aud" / str(counter["n"])
        sub.mkdir(parents=True, exist_ok=True)
        path = sub / name
        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(8000)
            wav.writeframes(struct.pack("<h", 0) * 8000)
        return str(path)

    return _make
