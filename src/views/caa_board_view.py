from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CAABoardView(QWidget):
    item_clicked = pyqtSignal(str)
    back_requested = pyqtSignal()
    generate_test_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        header_bar = QFrame()
        header_bar.setObjectName("headerBar")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 10, 20, 10)

        back_button = QPushButton("⬅ Volver al Dashboard")
        back_button.setObjectName("themeToggle")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(self.back_requested.emit)

        self.board_title = QLabel("Tablero CAA")
        self.board_title.setObjectName("headerTitle")

        header_layout.addWidget(back_button)
        header_layout.addWidget(self.board_title)
        header_layout.addStretch()

        self.grid_container = QFrame()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)

        root_layout.addWidget(header_bar)
        root_layout.addWidget(self.grid_container, 1)

    def _clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def render_board(self, board_data, items):
        self._clear_grid()
        self.board_title.setText(board_data.get("name", "Tablero CAA"))

        if not items:
            self._render_empty_state()
            return

        rows = board_data.get("grid_size", {}).get("rows", 2)
        cols = board_data.get("grid_size", {}).get("cols", 2)

        for item_data in items:
            position = item_data.get("position", [0, 0])
            row, col = position[0], position[1]
            if row >= rows or col >= cols:
                continue

            image_bytes = item_data.get("image_bytes")
            audio_path = item_data.get("audio_path", "")
            label = item_data.get("label", "")

            button = QPushButton()
            button.setFixedSize(200, 200)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            if image_bytes:
                pixmap = QPixmap()
                if pixmap.loadFromData(image_bytes):
                    scaled = pixmap.scaled(
                        200,
                        200,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    button.setIcon(QIcon(scaled))
                    button.setIconSize(button.size())
                else:
                    button.setText(label or "?")
            else:
                button.setText(label or "?")

            button.clicked.connect(
                lambda checked=False, path=audio_path: self.item_clicked.emit(path)
            )

            self.grid_layout.addWidget(button, row, col)

    def _render_empty_state(self):
        empty_label = QLabel(
            "Este paciente aun no tiene tableros CAA configurados."
        )
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("font-size: 14pt; color: #888;")

        generate_button = QPushButton("Generar Tablero de Prueba")
        generate_button.setObjectName("themeToggle")
        generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_button.clicked.connect(self.generate_test_requested.emit)

        placeholder = QWidget()
        placeholder_layout = QVBoxLayout(placeholder)
        placeholder_layout.addStretch()
        placeholder_layout.addWidget(
            empty_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        placeholder_layout.addWidget(
            generate_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        placeholder_layout.addStretch()

        self.grid_layout.addWidget(placeholder, 0, 0)
