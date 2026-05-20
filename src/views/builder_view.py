import os
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class BuilderView(QWidget):
    back_requested = pyqtSignal()
    board_save_requested = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._active_media = None
        self._board_data = self._default_board()
        self._cell_buttons = {}
        self._setup_ui()
        self._refresh_grid_labels()

    def _setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        header_bar = QFrame()
        header_bar.setObjectName("headerBar")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 10, 20, 10)

        back_button = QPushButton("⬅ Volver")
        back_button.setObjectName("themeToggle")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(self.back_requested.emit)

        self.header_title = QLabel("Constructor Visual CAA")
        self.header_title.setObjectName("headerTitle")

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()

        save_button = QPushButton("💾 Guardar Tablero")
        save_button.setObjectName("themeToggle")
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self._on_save_clicked)

        header_layout.addWidget(back_button)
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.message_label)
        header_layout.addWidget(save_button)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        gallery_panel = QFrame()
        gallery_panel.setObjectName("formPanel")
        gallery_panel.setFixedWidth(320)
        gallery_layout = QVBoxLayout(gallery_panel)
        gallery_layout.setContentsMargins(20, 20, 20, 20)
        gallery_layout.setSpacing(10)

        gallery_hint = QLabel("1. Selecciona un medio")
        gallery_hint.setStyleSheet("font-size: 11pt; font-weight: 600;")
        gallery_layout.addWidget(gallery_hint)

        images_label = QLabel("Imágenes")
        images_label.setStyleSheet("font-size: 10pt; font-weight: 500;")
        gallery_layout.addWidget(images_label)

        self.image_list = QListWidget()
        self.image_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.image_list.itemClicked.connect(self._on_image_selected)
        gallery_layout.addWidget(self.image_list)

        audios_label = QLabel("Audios")
        audios_label.setStyleSheet("font-size: 10pt; font-weight: 500;")
        gallery_layout.addWidget(audios_label)

        self.audio_list = QListWidget()
        self.audio_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.audio_list.itemClicked.connect(self._on_audio_selected)
        gallery_layout.addWidget(self.audio_list, 1)

        grid_panel = QFrame()
        grid_layout = QVBoxLayout(grid_panel)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(10)

        grid_hint = QLabel("2. Haz clic en una celda para asignarlo")
        grid_hint.setStyleSheet("font-size: 11pt; font-weight: 600;")
        grid_layout.addWidget(grid_hint)

        self.grid_container = QFrame()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        rows = self._board_data.get("grid_size", {}).get("rows", 2)
        cols = self._board_data.get("grid_size", {}).get("cols", 2)
        for row in range(rows):
            for col in range(cols):
                button = QPushButton()
                button.setFixedSize(200, 200)
                button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(
                    lambda checked=False, r=row, c=col: self._on_cell_clicked(r, c)
                )
                self.grid_layout.addWidget(button, row, col)
                self._cell_buttons[(row, col)] = button

        grid_layout.addWidget(self.grid_container, 1)

        body_layout.addWidget(gallery_panel)
        body_layout.addWidget(grid_panel, 1)

        root_layout.addWidget(header_bar)
        root_layout.addLayout(body_layout, 1)

    def set_gallery(self, images, audios):
        self.image_list.clear()
        self.audio_list.clear()
        self._active_media = None
        self.image_list.clearSelection()
        self.audio_list.clearSelection()

        for media in images or []:
            file_name = media.get("file_name", "")
            if not file_name:
                continue
            item = QListWidgetItem(file_name)
            item.setData(
                Qt.ItemDataRole.UserRole,
                {"file_name": file_name, "file_type": "image"},
            )
            self.image_list.addItem(item)

        for media in audios or []:
            file_name = media.get("file_name", "")
            if not file_name:
                continue
            item = QListWidgetItem(file_name)
            item.setData(
                Qt.ItemDataRole.UserRole,
                {"file_name": file_name, "file_type": "audio"},
            )
            self.audio_list.addItem(item)

    def reset_board(self):
        self._board_data = self._default_board()
        self._refresh_grid_labels()

    def show_message(self, text, is_error=False):
        color = "#d32f2f" if is_error else "#388e3c"
        self.message_label.setStyleSheet(f"font-size: 10pt; color: {color};")
        self.message_label.setText(text)
        self.message_label.show()
        QTimer.singleShot(3000, self.message_label.hide)

    def _default_board(self):
        items = []
        for row in range(2):
            for col in range(2):
                items.append(
                    {
                        "position": [row, col],
                        "label": "",
                        "image_file": "",
                        "audio_file": "",
                    }
                )
        return {
            "id": "board_01",
            "name": "Tablero CAA",
            "grid_size": {"rows": 2, "cols": 2},
            "items": items,
        }

    def _on_image_selected(self, item):
        self.audio_list.clearSelection()
        self._active_media = item.data(Qt.ItemDataRole.UserRole)

    def _on_audio_selected(self, item):
        self.image_list.clearSelection()
        self._active_media = item.data(Qt.ItemDataRole.UserRole)

    def _on_cell_clicked(self, row, col):
        if not self._active_media:
            return

        file_name = self._active_media.get("file_name", "")
        file_type = self._active_media.get("file_type", "")
        if not file_name:
            return

        cell_item = self._get_cell_item(row, col)
        if not cell_item:
            return

        if file_type == "image":
            cell_item["image_file"] = file_name
        elif file_type == "audio":
            cell_item["audio_file"] = file_name
            cell_item["label"] = self._label_from_audio(file_name)

        self._refresh_cell_label(row, col)

    def _on_save_clicked(self):
        self.board_save_requested.emit(self._board_data)

    def _get_cell_item(self, row, col):
        for item in self._board_data.get("items", []):
            if item.get("position") == [row, col]:
                return item
        return None

    def _label_from_audio(self, file_name):
        base = os.path.splitext(file_name)[0]
        return base or file_name

    def _cell_text(self, item):
        if not item:
            return "Sin asignar"

        image_file = item.get("image_file", "")
        audio_file = item.get("audio_file", "")
        label = item.get("label", "")
        parts = []

        if image_file:
            parts.append(f"IMG: {image_file}")
        if audio_file:
            parts.append(f"AUD: {label or audio_file}")

        return "\n".join(parts) if parts else "Sin asignar"

    def _refresh_cell_label(self, row, col):
        button = self._cell_buttons.get((row, col))
        if not button:
            return
        item = self._get_cell_item(row, col)
        button.setText(self._cell_text(item))

    def _refresh_grid_labels(self):
        for (row, col) in self._cell_buttons:
            self._refresh_cell_label(row, col)
