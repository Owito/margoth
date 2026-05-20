import os
from PyQt6.QtWidgets import QApplication
from utils.path_resolver import PathResolver

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.styles_dir = PathResolver.get_resource_path(
            os.path.join("assets", "styles")
        )

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
