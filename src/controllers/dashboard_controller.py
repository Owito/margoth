class DashboardController:
    def __init__(self, view, patient_model):
        self._view = view
        self._model = patient_model
        self._view.patient_save_requested.connect(self._on_save_patient)
        self._view.patient_update_requested.connect(self._on_update_patient)
        self._view.patient_delete_requested.connect(self._on_delete_patient)
        self._view.edit_requested.connect(self._on_edit_requested)
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

    def _on_edit_requested(self, patient_ref):
        patient = self._model.get_patient_by_id(patient_ref.get("id"))
        if patient:
            self._view.enter_edit_mode(patient)

    def _on_update_patient(self, patient_id, data):
        self._model.update_patient(
            patient_id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"],
            notes=data["notes"],
        )
        self.load_patients()
        self._view.show_message("Paciente actualizado correctamente")

    def _on_delete_patient(self, patient_id):
        if self._model.delete_patient(patient_id):
            self.load_patients()
            self._view.show_message("Paciente eliminado")
        else:
            self._view.show_message("No se pudo eliminar el paciente", is_error=True)

    def load_patients(self):
        patients = self._model.get_all_patients()
        self._view.populate_table(patients)

    def _on_upload_media(self, patient_ref, source_path, label=""):
        patient_id = patient_ref.get("id")
        result = self._model.import_media(patient_id, source_path, label=label)
        if result:
            self._view.show_message(
                f"Archivo '{result}' importado correctamente"
            )
        else:
            self._view.show_message("Error al importar archivo", is_error=True)
