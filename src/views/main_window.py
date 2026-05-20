from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

class MainWindow(QMainWindow):
    theme_toggle_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Margoth - Rehabilitación Cognitiva")
        self.resize(1024, 768)
        self.setup_ui()

    def setup_ui(self):
        # Widget central (Cero sobrecarga cognitiva)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Bar (Frame en lugar de QMenuBar)
        header_bar = QFrame()
        header_bar.setObjectName("headerBar")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Título en el Header
        app_title = QLabel("Margoth")
        app_title.setObjectName("headerTitle")

        # Spacer para empujar el botón a la derecha
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Botón Toggle Tema
        self.theme_btn = QPushButton("\U0001f319 Modo Oscuro")
        self.theme_btn.setObjectName("themeToggle")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.theme_toggle_requested.emit)

        header_layout.addWidget(app_title)
        header_layout.addItem(spacer)
        header_layout.addWidget(self.theme_btn)

        # Área Central (Placeholder para futuros tableros/ejercicios)
        content_area = QFrame()
        content_layout = QVBoxLayout(content_area)

        welcome_label = QLabel("Panel Principal\n(Seleccione un paciente o inicie sesión)")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(welcome_label)

        # Ensamblar layout principal
        main_layout.addWidget(header_bar)
        main_layout.addWidget(content_area)

    def update_theme_button(self, current_theme):
        if current_theme == "dark":
            self.theme_btn.setText("\u2600\ufe0f Modo Claro")
        else:
            self.theme_btn.setText("\U0001f319 Modo Oscuro")
