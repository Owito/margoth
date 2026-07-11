class BuilderController:
    def __init__(self, view, patient_model, caa_model):
        self._view = view
        self._patient_model = patient_model
        self._caa_model = caa_model
        self._current_patient = None

        self._view.board_save_requested.connect(self._on_save_requested)
        self._view.board_selected.connect(self._on_board_selected)
        self._view.new_board_requested.connect(self._on_new_board)

    @property
    def view(self):
        return self._view

    def load_patient(self, patient_dict):
        self._current_patient = patient_dict
        patient_id = patient_dict.get("id")
        images = self._patient_model.get_patient_media(patient_id, "image")
        audios = self._patient_model.get_patient_media(patient_id, "audio")
        self._view.set_gallery(images, audios)
        self._refresh_boards()

    def _refresh_boards(self, active_id=None):
        boards = self._caa_model.list_boards(self._current_patient)
        self._view.set_boards(boards, active_id)
        if boards:
            target = active_id or boards[0]["id"]
            board, _ = self._caa_model.load_board(self._current_patient, target)
            self._view.load_board_data(board)
        else:
            self._view.new_board()

    def _on_board_selected(self, board_id):
        board, _ = self._caa_model.load_board(self._current_patient, board_id)
        self._view.load_board_data(board)

    def _on_new_board(self):
        self._view.new_board()

    def _on_save_requested(self, board_data):
        if not self._current_patient:
            self._view.show_message("Paciente no válido", is_error=True)
            return

        saved = self._caa_model.save_board(self._current_patient, board_data)
        if saved:
            self._view.show_message("Tablero guardado correctamente")
            # Refresca el selector conservando el tablero recién guardado activo
            boards = self._caa_model.list_boards(self._current_patient)
            active = board_data.get("id") or (boards[-1]["id"] if boards else None)
            self._view.set_boards(boards, active)
        else:
            self._view.show_message("Error guardando tablero", is_error=True)
