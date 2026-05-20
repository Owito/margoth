from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SemanticExerciseView(QWidget):
    answer_selected = pyqtSignal(str)
    exit_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._option_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        header_bar = QFrame()
        header_bar.setObjectName("headerBar")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 10, 20, 10)

        back_button = QPushButton("⬅ Terminar Ejercicio")
        back_button.setObjectName("themeToggle")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(self.exit_requested.emit)

        self.header_title = QLabel("Ejercicio Semántico")
        self.header_title.setObjectName("headerTitle")

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.hide()

        header_layout.addWidget(back_button)
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.feedback_label)

        center_panel = QFrame()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(20)

        self.image_label = QLabel("")
        self.image_label.setFixedSize(400, 400)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ddd; background: #fff;")
        center_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        options_panel = QFrame()
        options_layout = QHBoxLayout(options_panel)
        options_layout.setSpacing(12)

        for _ in range(3):
            button = QPushButton("Opción")
            button.setObjectName("themeToggle")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.setMinimumHeight(60)
            button.clicked.connect(self._emit_answer)
            self._option_buttons.append(button)
            options_layout.addWidget(button)

        center_layout.addWidget(options_panel)

        root_layout.addWidget(header_bar)
        root_layout.addWidget(center_panel, 1)

    def render_stimulus(self, image_bytes, options_list):
        if image_bytes:
            pixmap = QPixmap()
            if pixmap.loadFromData(image_bytes):
                scaled = pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.image_label.setPixmap(scaled)
                self.image_label.setText("")
            else:
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText("Imagen inválida")
        else:
            self.image_label.setPixmap(QPixmap())
            self.image_label.setText("Sin imagen")

        for idx, button in enumerate(self._option_buttons):
            text = options_list[idx] if idx < len(options_list) else "Opción"
            button.setText(text)

    def show_feedback(self, text, is_error=False):
        color = "#d32f2f" if is_error else "#388e3c"
        self.feedback_label.setStyleSheet(f"font-size: 11pt; color: {color};")
        self.feedback_label.setText(text)
        self.feedback_label.show()
        QTimer.singleShot(1000, self.feedback_label.hide)

    def _emit_answer(self):
        button = self.sender()
        if not button:
            return
        self.answer_selected.emit(button.text())
