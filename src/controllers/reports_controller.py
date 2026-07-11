class ReportsController:
    def __init__(self, view, metrics_model):
        self._view = view
        self._model = metrics_model
        self._current_patient = None

    @property
    def view(self):
        return self._view

    def load_report(self, patient_dict):
        self._current_patient = patient_dict
        patient_id = patient_dict.get("id")
        name = f"{patient_dict.get('first_name', '')} {patient_dict.get('last_name', '')}".strip()

        summary = self._model.get_patient_summary(patient_id)
        recent = self._model.get_recent_attempts(patient_id)
        daily = self._model.get_daily_accuracy(patient_id)
        self._view.render_report(name, summary, recent, daily)
