from views.main_window import MainWindow


class AppController:
    def __init__(self, theme_manager, db_manager=None, patient_model=None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.patient_model = patient_model
        self.main_window = MainWindow()

        self.main_window.theme_toggle_requested.connect(self._on_theme_toggle)

    def show_main_window(self):
        self.main_window.show()

    def _on_theme_toggle(self):
        new_theme = self.theme_manager.toggle_theme()
        self.main_window.update_theme_button(new_theme)
