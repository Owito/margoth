from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QFormLayout,
    QLineEdit, QDateEdit, QPlainTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFileDialog, QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate


class DashboardView(QWidget):
    patient_save_requested = pyqtSignal(dict)
    caa_requested = pyqtSignal(dict)
    upload_requested = pyqtSignal(dict, str)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Panel izquierdo: formulario ──────────────────────────
        form_panel = QFrame()
        form_panel.setObjectName("formPanel")
        form_panel.setFixedWidth(300)
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(20, 20, 20, 20)

        fields = QFormLayout()
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Nombre del paciente")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Apellido del paciente")

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDisplayFormat("dd/MM/yyyy")
        self.birth_date_input.setDate(QDate.currentDate())

        self.notes_input = QPlainTextEdit()
        self.notes_input.setPlaceholderText("Notas clínicas opcionales...")
        self.notes_input.setMaximumHeight(100)

        fields.addRow("Nombres:", self.first_name_input)
        fields.addRow("Apellidos:", self.last_name_input)
        fields.addRow("F. Nacimiento:", self.birth_date_input)
        fields.addRow("Notas:", self.notes_input)
        form_layout.addLayout(fields)

        self.save_btn = QPushButton("Guardar Paciente")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self._on_save_clicked)
        form_layout.addWidget(self.save_btn)
        form_layout.addStretch()

        # ── Panel derecho: tabla ─────────────────────────────────
        table_panel = QFrame()
        table_panel.setObjectName("tablePanel")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(10, 20, 20, 20)

        self.patients_table = QTableWidget()
        self.patients_table.setColumnCount(4)
        self.patients_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Acciones"])
        self.patients_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.patients_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.patients_table.horizontalHeader().setStretchLastSection(True)
        self.patients_table.verticalHeader().setVisible(False)
        self.patients_table.itemSelectionChanged.connect(self._on_selection_changed)
        table_layout.addWidget(self.patients_table)

        self.caa_btn = QPushButton("Abrir Tablero CAA")
        self.caa_btn.setObjectName("themeToggle")
        self.caa_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.caa_btn.setEnabled(False)
        self.caa_btn.clicked.connect(self._on_caa_clicked)
        table_layout.addWidget(self.caa_btn)

        self.upload_btn = QPushButton("Subir Archivo (Foto/Audio)")
        self.upload_btn.setObjectName("themeToggle")
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self._on_upload_clicked)
        table_layout.addWidget(self.upload_btn)

        self.message_label = QLabel("")
        self.message_label.setObjectName("messageLabel")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 10pt; color: #666;")
        self.message_label.hide()
        table_layout.addWidget(self.message_label)

        # ── Ensamblar ────────────────────────────────────────────
        root_layout.addWidget(form_panel)
        root_layout.addWidget(table_panel, 1)

    def _on_save_clicked(self):
        data = {
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "birth_date": self.birth_date_input.date().toString("yyyy-MM-dd"),
            "notes": self.notes_input.toPlainText().strip(),
        }
        if data["first_name"] and data["last_name"]:
            self.patient_save_requested.emit(data)

    def _on_selection_changed(self):
        has_selection = len(self.patients_table.selectedItems()) > 0
        self.caa_btn.setEnabled(has_selection)
        self.upload_btn.setEnabled(has_selection)

    def _on_caa_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.caa_requested.emit({"id": patient_id})

    def _on_upload_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return

        patient_id = int(self.patients_table.item(row, 0).text())
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo multimedia",
            "",
            "Im\u00e1genes (*.png *.jpg *.jpeg);;Audios (*.mp3 *.wav)",
        )
        if file_path:
            self.upload_requested.emit({"id": patient_id}, file_path)

    def show_message(self, text, is_error=False):
        color = "#d32f2f" if is_error else "#388e3c"
        self.message_label.setStyleSheet(f"font-size: 10pt; color: {color};")
        self.message_label.setText(text)
        self.message_label.show()

        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, self.message_label.hide)

    def clear_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.birth_date_input.setDate(QDate.currentDate())
        self.notes_input.clear()

    def populate_table(self, patients: list):
        self.patients_table.setRowCount(len(patients))
        for row, p in enumerate(patients):
            self.patients_table.setItem(row, 0, QTableWidgetItem(str(p["id"])))
            self.patients_table.setItem(row, 1, QTableWidgetItem(p["first_name"]))
            self.patients_table.setItem(row, 2, QTableWidgetItem(p["last_name"]))
            self.patients_table.setItem(row, 3, QTableWidgetItem(""))
