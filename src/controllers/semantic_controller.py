import time
from PyQt6.QtCore import QTimer


class SemanticController:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._current_patient = None
        self._correct_answer = ""
        self._start_time = None

        self._view.answer_selected.connect(self._on_answer_selected)

    @property
    def view(self):
        return self._view

    def start_exercise(self, patient_dict):
        self._current_patient = patient_dict
        self._load_next_stimulus()

    def _load_next_stimulus(self):
        if not self._current_patient:
            return

        patient_id = self._current_patient.get("id")
        stimulus = self._model.get_next_stimulus(patient_id)
        if not stimulus:
            self._view.show_feedback("Sin imágenes disponibles", is_error=True)
            return

        self._correct_answer = stimulus.get("correct_answer", "")
        self._start_time = time.perf_counter()
        self._view.render_stimulus(
            stimulus.get("image_bytes"),
            stimulus.get("options", []),
        )

    def _on_answer_selected(self, answer):
        if not self._current_patient or self._start_time is None:
            return

        reaction_time_ms = (time.perf_counter() - self._start_time) * 1000
        is_correct = answer == self._correct_answer

        patient_id = self._current_patient.get("id")
        self._model.save_metric(patient_id, is_correct, reaction_time_ms)

        self._start_time = None

        if is_correct:
            self._view.show_feedback("¡Muy bien!")
        else:
            self._view.show_feedback("Intenta de nuevo", is_error=True)

        QTimer.singleShot(1000, self._load_next_stimulus)
