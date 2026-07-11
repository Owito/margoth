import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from models.database_manager import DatabaseManager
from models.patient_model import PatientModel
from controllers.app_controller import AppController
from utils.theme_manager import ThemeManager
from utils.path_resolver import PathResolver


def main():
    db_manager = DatabaseManager()
    db_manager.initialize_database()

    patient_model = PatientModel(db_manager)

    app = QApplication(sys.argv)
    app.setApplicationName("Margoth")

    icon_path = PathResolver.get_resource_path(os.path.join("assets", "icon.png"))
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    theme_manager = ThemeManager()
    theme_manager.apply_theme("light")

    controller = AppController(theme_manager, db_manager=db_manager, patient_model=patient_model)
    controller.show_main_window()

    exit_code = app.exec()
    db_manager.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
