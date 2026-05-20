import os
from PyQt6.QtWidgets import QApplication

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        # Resuelve la ruta absoluta hacia assets/styles independientemente desde dónde se ejecute
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.styles_dir = os.path.join(base_dir, 'assets', 'styles')

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        qss_path = os.path.join(self.styles_dir, f"{theme_name}.qss")

        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                qss_content = f.read()
                app = QApplication.instance()
                if app:
                    app.setStyleSheet(qss_content)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema {qss_path}")

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        return new_theme
