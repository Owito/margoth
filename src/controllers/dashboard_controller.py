class DashboardController:
    def __init__(self, view, patient_model):
        self._view = view
        self._model = patient_model
        self._view.patient_save_requested.connect(self._on_save_patient)
        self._view.upload_requested.connect(self._on_upload_media)

    def initialize(self):
        self.load_patients()

    def _on_save_patient(self, data):
        self._model.create_patient(
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"],
            notes=data["notes"],
        )
        self._view.clear_form()
        self.load_patients()

    def load_patients(self):
        patients = self._model.get_all_patients()
        self._view.populate_table(patients)

    def _on_upload_media(self, patient_ref, source_path):
        patient_id = patient_ref.get("id")
        result = self._model.import_media(patient_id, source_path)
        if result:
            self._view.show_message(
                f"Archivo '{result}' importado correctamente"
            )
        else:
            self._view.show_message("Error al importar archivo", is_error=True)
