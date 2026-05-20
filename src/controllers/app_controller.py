from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from controllers.dashboard_controller import DashboardController
from controllers.caa_controller import CAAController


class AppController:
    def __init__(self, theme_manager, db_manager=None, patient_model=None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.patient_model = patient_model
        self.main_window = MainWindow()

        self.main_window.theme_toggle_requested.connect(self._on_theme_toggle)

        # Dashboard del terapeuta
        self.dashboard_view = DashboardView()
        self.dashboard_controller = DashboardController(self.dashboard_view, self.patient_model)
        self.caa_controller = CAAController(self.db_manager)
        self.dashboard_view.caa_requested.connect(self._on_caa_requested)
        self.caa_controller.view.back_requested.connect(self._on_caa_back)
        self.main_window.set_main_view(self.dashboard_view)
        self.dashboard_controller.initialize()

    def show_main_window(self):
        self.main_window.show()

    def _on_theme_toggle(self):
        new_theme = self.theme_manager.toggle_theme()
        self.main_window.update_theme_button(new_theme)

    def _on_caa_requested(self, patient_ref):
        patient_id = patient_ref.get("id")
        patient_dict = self.patient_model.get_patient_by_id(patient_id)
        if patient_dict:
            self.caa_controller.load_patient_board(patient_dict)
            self.main_window.set_main_view(self.caa_controller.view)

    def _on_caa_back(self):
        self.main_window.set_main_view(self.dashboard_view)
