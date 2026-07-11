import os
import uuid
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

MAX_GRID = 4


class BuilderView(QWidget):
    back_requested = pyqtSignal()
    board_save_requested = pyqtSignal(dict)
    board_selected = pyqtSignal(str)
    new_board_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._active_media = None
        self._board_data = self._default_board()
        self._cell_buttons = {}
        self._setup_ui()
        self._rebuild_grid()

    # ── Construcción de UI ────────────────────────────────────────
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

        self.board_selector = QComboBox()
        self.board_selector.setMinimumWidth(180)
        self.board_selector.currentIndexChanged.connect(self._on_board_selected)

        new_button = QPushButton("➕ Nuevo")
        new_button.setObjectName("themeToggle")
        new_button.setCursor(Qt.CursorShape.PointingHandCursor)
        new_button.clicked.connect(self.new_board_requested.emit)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()

        save_button = QPushButton("💾 Guardar Tablero")
        save_button.setObjectName("themeToggle")
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self._on_save_clicked)

        header_layout.addWidget(back_button)
        header_layout.addWidget(self.header_title)
        header_layout.addSpacing(12)
        header_layout.addWidget(QLabel("Tablero:"))
        header_layout.addWidget(self.board_selector)
        header_layout.addWidget(new_button)
        header_layout.addStretch()
        header_layout.addWidget(self.message_label)
        header_layout.addWidget(save_button)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # ── Galería (izquierda) ──
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

        # ── Grilla (derecha) ──
        grid_panel = QFrame()
        grid_layout = QVBoxLayout(grid_panel)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(10)

        # Fila de configuración del tablero
        config_row = QHBoxLayout()
        config_row.addWidget(QLabel("Nombre:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del tablero")
        config_row.addWidget(self.name_input, 1)

        config_row.addWidget(QLabel("Filas:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, MAX_GRID)
        config_row.addWidget(self.rows_spin)

        config_row.addWidget(QLabel("Columnas:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, MAX_GRID)
        config_row.addWidget(self.cols_spin)

        apply_btn = QPushButton("Aplicar tamaño")
        apply_btn.setObjectName("themeToggle")
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.clicked.connect(self._on_apply_size)
        config_row.addWidget(apply_btn)
        grid_layout.addLayout(config_row)

        grid_hint = QLabel("2. Haz clic en una celda para asignar el medio")
        grid_hint.setStyleSheet("font-size: 11pt; font-weight: 600;")
        grid_layout.addWidget(grid_hint)

        # Contenedor de grilla dentro de un scroll (para tamaños grandes)
        self.grid_container = QFrame()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grid_container)
        grid_layout.addWidget(scroll, 1)

        body_layout.addWidget(gallery_panel)
        body_layout.addWidget(grid_panel, 1)

        root_layout.addWidget(header_bar)
        root_layout.addLayout(body_layout, 1)

        self._sync_size_spins()

    # ── Galería ───────────────────────────────────────────────────
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
            item = QListWidgetItem(self._display_text(media))
            item.setData(
                Qt.ItemDataRole.UserRole,
                {"file_name": file_name, "file_type": "image"},
            )
            self.image_list.addItem(item)

        for media in audios or []:
            file_name = media.get("file_name", "")
            if not file_name:
                continue
            item = QListWidgetItem(self._display_text(media))
            item.setData(
                Qt.ItemDataRole.UserRole,
                {"file_name": file_name, "file_type": "audio"},
            )
            self.audio_list.addItem(item)

    @staticmethod
    def _display_text(media):
        label = (media.get("label") or "").strip()
        file_name = media.get("file_name", "")
        return f"{label}  ·  {file_name}" if label else file_name

    # ── Selector de tableros ──────────────────────────────────────
    def set_boards(self, boards, active_id=None):
        """Rellena el combo de tableros sin disparar la señal de selección."""
        self.board_selector.blockSignals(True)
        self.board_selector.clear()
        for board in boards:
            self.board_selector.addItem(board.get("name", "Tablero"), board.get("id"))
        if active_id is not None:
            idx = self.board_selector.findData(active_id)
            if idx >= 0:
                self.board_selector.setCurrentIndex(idx)
        self.board_selector.blockSignals(False)

    def _on_board_selected(self, _index):
        board_id = self.board_selector.currentData()
        if board_id:
            self.board_selected.emit(board_id)

    # ── Carga / creación de tableros ──────────────────────────────
    def load_board_data(self, board):
        """Carga un tablero (crudo) en el editor."""
        self._board_data = self._normalize_board(board)
        self.name_input.setText(self._board_data.get("name", ""))
        self._sync_size_spins()
        self._rebuild_grid()

    def new_board(self):
        self._board_data = self._default_board()
        self.name_input.setText(self._board_data["name"])
        self._sync_size_spins()
        self._rebuild_grid()
        # Deseleccionar el combo para indicar que es un tablero nuevo
        self.board_selector.blockSignals(True)
        self.board_selector.setCurrentIndex(-1)
        self.board_selector.blockSignals(False)

    def reset_board(self):
        """Compatibilidad: reinicia a un tablero nuevo por defecto."""
        self.new_board()

    def show_message(self, text, is_error=False):
        color = "#d32f2f" if is_error else "#388e3c"
        self.message_label.setStyleSheet(f"font-size: 10pt; color: {color};")
        self.message_label.setText(text)
        self.message_label.show()
        QTimer.singleShot(3000, self.message_label.hide)

    # ── Modelo interno del tablero ────────────────────────────────
    def _default_board(self):
        return self._normalize_board(
            {
                "id": f"board_{uuid.uuid4().hex[:8]}",
                "name": "Tablero CAA",
                "grid_size": {"rows": 2, "cols": 2},
                "items": [],
            }
        )

    def _normalize_board(self, board):
        """Garantiza id/nombre/tamaño y un item por cada celda de la grilla."""
        grid = board.get("grid_size") or {}
        rows = self._clamp(grid.get("rows", 2))
        cols = self._clamp(grid.get("cols", 2))

        existentes = {
            tuple(item.get("position", [-1, -1])): item for item in board.get("items", [])
        }
        items = []
        for row in range(rows):
            for col in range(cols):
                prev = existentes.get((row, col), {})
                items.append(
                    {
                        "position": [row, col],
                        "label": prev.get("label", ""),
                        "image_file": prev.get("image_file", ""),
                        "audio_file": prev.get("audio_file", ""),
                    }
                )
        return {
            "id": board.get("id", ""),
            "name": board.get("name", "Tablero CAA"),
            "grid_size": {"rows": rows, "cols": cols},
            "items": items,
        }

    @staticmethod
    def _clamp(value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            return 2
        return max(1, min(MAX_GRID, value))

    def _sync_size_spins(self):
        grid = self._board_data.get("grid_size", {})
        self.rows_spin.setValue(self._clamp(grid.get("rows", 2)))
        self.cols_spin.setValue(self._clamp(grid.get("cols", 2)))

    def _on_apply_size(self):
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        self._board_data["grid_size"] = {"rows": rows, "cols": cols}
        # Renormaliza preservando asignaciones dentro del nuevo rango
        self._board_data = self._normalize_board(self._board_data)
        self._rebuild_grid()

    # ── Grilla ────────────────────────────────────────────────────
    def _rebuild_grid(self):
        # Limpia botones anteriores
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._cell_buttons = {}

        rows = self._board_data["grid_size"]["rows"]
        cols = self._board_data["grid_size"]["cols"]
        for row in range(rows):
            for col in range(cols):
                button = QPushButton()
                button.setMinimumSize(150, 150)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.clicked.connect(
                    lambda checked=False, r=row, c=col: self._on_cell_clicked(r, c)
                )
                self.grid_layout.addWidget(button, row, col)
                self._cell_buttons[(row, col)] = button
        self._refresh_grid_labels()

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
        self._board_data["name"] = self.name_input.text().strip() or "Tablero CAA"
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
