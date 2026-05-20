import sys
import os

# Forzar que el directorio 'src' esté en el path para facilitar imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from controllers.app_controller import AppController
from utils.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Margoth")

    # Inicializar gestor de temas y cargar el tema claro por defecto
    theme_manager = ThemeManager()
    theme_manager.apply_theme("light")

    # Inyectar el gestor en el controlador y levantar la vista principal
    controller = AppController(theme_manager)
    controller.show_main_window()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
