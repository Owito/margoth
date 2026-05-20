from views.main_window import MainWindow

class AppController:
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.main_window = MainWindow()

        # Conectar señales de la vista a las acciones del controlador
        self.main_window.theme_toggle_requested.connect(self._on_theme_toggle)

    def show_main_window(self):
        self.main_window.show()

    def _on_theme_toggle(self):
        new_theme = self.theme_manager.toggle_theme()
        self.main_window.update_theme_button(new_theme)
