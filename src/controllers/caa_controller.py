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
        self._view.board_change_requested.connect(self._on_board_changed)

    @property
    def view(self):
        return self._view

    def load_patient_board(self, patient_dict):
        self._current_patient = patient_dict
        boards = self._model.list_boards(patient_dict)
        active_id = boards[0]["id"] if boards else None
        self._view.set_boards(boards, active_id)
        board, items = self._model.load_board(patient_dict, active_id)
        self._view.render_board(board, items)

    def _on_board_changed(self, board_id):
        if not self._current_patient:
            return
        board, items = self._model.load_board(self._current_patient, board_id)
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
