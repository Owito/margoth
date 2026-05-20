from models.caa_board_model import CAABoardModel
from utils.audio_player import AudioPlayer
from views.caa_board_view import CAABoardView


class CAAController:
    def __init__(self, db_manager):
        self._model = CAABoardModel(db_manager)
        self._audio_player = AudioPlayer()
        self._view = CAABoardView()
        self._current_patient = None

        self._view.item_clicked.connect(self._on_item_clicked)
        self._view.generate_test_requested.connect(self._on_generate_test)

    @property
    def view(self):
        return self._view

    def load_patient_board(self, patient_dict):
        self._current_patient = patient_dict
        board, items = self._model.load_first_board(patient_dict)
        self._view.render_board(board, items)

    def _on_item_clicked(self, audio_path):
        if not audio_path:
            return
        audio_bytes = self._model.load_audio_bytes(audio_path)
        if audio_bytes:
            self._audio_player.play_audio(audio_bytes)

    def _on_generate_test(self):
        if not self._current_patient:
            return
        self._model.create_test_board(self._current_patient)
        self.load_patient_board(self._current_patient)
