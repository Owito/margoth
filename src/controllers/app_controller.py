from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from controllers.dashboard_controller import DashboardController


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
        self.main_window.set_main_view(self.dashboard_view)
        self.dashboard_controller.initialize()

    def show_main_window(self):
        self.main_window.show()

    def _on_theme_toggle(self):
        new_theme = self.theme_manager.toggle_theme()
        self.main_window.update_theme_button(new_theme)
