from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QFormLayout,
    QLineEdit, QDateEdit, QPlainTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFileDialog, QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate


class DashboardView(QWidget):
    patient_save_requested = pyqtSignal(dict)
    patient_update_requested = pyqtSignal(int, dict)
    patient_delete_requested = pyqtSignal(int)
    edit_requested = pyqtSignal(dict)
    caa_requested = pyqtSignal(dict)
    builder_requested = pyqtSignal(dict)
    exercise_requested = pyqtSignal(dict)
    reports_requested = pyqtSignal(dict)
    upload_requested = pyqtSignal(dict, str, str)

    def __init__(self):
        super().__init__()
        self._editing_id = None      # None = alta; int = edición en curso
        self._delete_armed_id = None  # confirmación de borrado en dos pasos
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

        self.cancel_edit_btn = QPushButton("Cancelar edición")
        self.cancel_edit_btn.setObjectName("themeToggle")
        self.cancel_edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_edit_btn.clicked.connect(self._exit_edit_mode)
        self.cancel_edit_btn.hide()
        form_layout.addWidget(self.cancel_edit_btn)
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

        actions_row = QHBoxLayout()
        self.edit_btn = QPushButton("Editar Paciente")
        self.edit_btn.setObjectName("themeToggle")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self._on_edit_clicked)
        actions_row.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Eliminar Paciente")
        self.delete_btn.setObjectName("themeToggle")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        actions_row.addWidget(self.delete_btn)
        table_layout.addLayout(actions_row)

        self.caa_btn = QPushButton("Abrir Tablero CAA")
        self.caa_btn.setObjectName("themeToggle")
        self.caa_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.caa_btn.setEnabled(False)
        self.caa_btn.clicked.connect(self._on_caa_clicked)
        table_layout.addWidget(self.caa_btn)

        self.builder_btn = QPushButton("Constructor Visual")
        self.builder_btn.setObjectName("themeToggle")
        self.builder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.builder_btn.setEnabled(False)
        self.builder_btn.clicked.connect(self._on_builder_clicked)
        table_layout.addWidget(self.builder_btn)

        self.exercise_btn = QPushButton("Iniciar Ejercicio Semántico")
        self.exercise_btn.setObjectName("themeToggle")
        self.exercise_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exercise_btn.setEnabled(False)
        self.exercise_btn.clicked.connect(self._on_exercise_clicked)
        table_layout.addWidget(self.exercise_btn)

        self.reports_btn = QPushButton("Ver Reportes de Progreso")
        self.reports_btn.setObjectName("themeToggle")
        self.reports_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reports_btn.setEnabled(False)
        self.reports_btn.clicked.connect(self._on_reports_clicked)
        table_layout.addWidget(self.reports_btn)

        self.media_label_input = QLineEdit()
        self.media_label_input.setPlaceholderText(
            "Etiqueta del medio (ej. 'Agua'). Opcional: si se deja vacía se usa el nombre del archivo."
        )
        self.media_label_input.setEnabled(False)
        table_layout.addWidget(self.media_label_input)

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
        if not (data["first_name"] and data["last_name"]):
            self.show_message("Nombre y apellido son obligatorios", is_error=True)
            return

        if self._editing_id is None:
            self.patient_save_requested.emit(data)
        else:
            self.patient_update_requested.emit(self._editing_id, data)
            self._exit_edit_mode()

    def _on_edit_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.edit_requested.emit({"id": patient_id})

    def enter_edit_mode(self, patient):
        """Carga el paciente en el formulario para editarlo."""
        self._editing_id = patient.get("id")
        self.first_name_input.setText(patient.get("first_name", ""))
        self.last_name_input.setText(patient.get("last_name", ""))
        birth = patient.get("birth_date")
        if birth:
            self.birth_date_input.setDate(QDate.fromString(str(birth), "yyyy-MM-dd"))
        self.notes_input.setPlainText(patient.get("notes") or "")
        self.save_btn.setText("Actualizar Paciente")
        self.cancel_edit_btn.show()

    def _exit_edit_mode(self):
        self._editing_id = None
        self.save_btn.setText("Guardar Paciente")
        self.cancel_edit_btn.hide()
        self.clear_form()

    def _on_delete_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())

        # Confirmación en dos pasos (sin modales): primer clic arma, segundo borra
        if self._delete_armed_id != patient_id:
            self._delete_armed_id = patient_id
            self.delete_btn.setText("Confirmar Eliminación")
            self.show_message(
                "Clic de nuevo en 'Confirmar Eliminación' para borrar de forma permanente",
                is_error=True,
            )
            return

        self._disarm_delete()
        self.patient_delete_requested.emit(patient_id)

    def _disarm_delete(self):
        self._delete_armed_id = None
        self.delete_btn.setText("Eliminar Paciente")

    def _on_selection_changed(self):
        self._disarm_delete()  # cambiar de fila cancela un borrado armado
        has_selection = len(self.patients_table.selectedItems()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.caa_btn.setEnabled(has_selection)
        self.builder_btn.setEnabled(has_selection)
        self.exercise_btn.setEnabled(has_selection)
        self.reports_btn.setEnabled(has_selection)
        self.upload_btn.setEnabled(has_selection)
        self.media_label_input.setEnabled(has_selection)

    def _on_caa_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.caa_requested.emit({"id": patient_id})

    def _on_builder_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.builder_requested.emit({"id": patient_id})

    def _on_exercise_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.exercise_requested.emit({"id": patient_id})

    def _on_reports_clicked(self):
        row = self.patients_table.currentRow()
        if row < 0:
            return
        patient_id = int(self.patients_table.item(row, 0).text())
        self.reports_requested.emit({"id": patient_id})

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
            label = self.media_label_input.text().strip()
            self.upload_requested.emit({"id": patient_id}, file_path, label)
            self.media_label_input.clear()

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
