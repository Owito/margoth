class BuilderController:
    def __init__(self, view, patient_model, caa_model):
        self._view = view
        self._patient_model = patient_model
        self._caa_model = caa_model
        self._current_patient = None

        self._view.board_save_requested.connect(self._on_save_requested)

    @property
    def view(self):
        return self._view

    def load_patient(self, patient_dict):
        self._current_patient = patient_dict
        patient_id = patient_dict.get("id")
        images = self._patient_model.get_patient_media(patient_id, "image")
        audios = self._patient_model.get_patient_media(patient_id, "audio")
        self._view.set_gallery(images, audios)
        self._view.reset_board()

    def _on_save_requested(self, board_data):
        if not self._current_patient:
            self._view.show_message("Paciente no válido", is_error=True)
            return

        saved = self._caa_model.save_board(self._current_patient, board_data)
        if saved:
            self._view.show_message("Tablero guardado correctamente")
        else:
            self._view.show_message("Error guardando tablero", is_error=True)
