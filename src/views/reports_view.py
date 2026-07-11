from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ReportsView(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._stat_labels = {}
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

        self.header_title = QLabel("Reportes de Progreso")
        self.header_title.setObjectName("headerTitle")

        header_layout.addWidget(back_button)
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()

        body = QFrame()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 20)
        body_layout.setSpacing(16)

        # ── Tarjetas de estadísticas ──────────────────────────────
        self.stats_panel = QFrame()
        stats_layout = QGridLayout(self.stats_panel)
        stats_layout.setSpacing(12)

        self._add_stat_card(stats_layout, 0, 0, "total", "Intentos totales")
        self._add_stat_card(stats_layout, 0, 1, "accuracy", "Aciertos")
        self._add_stat_card(stats_layout, 0, 2, "avg", "Tiempo promedio")
        self._add_stat_card(stats_layout, 0, 3, "best", "Mejor tiempo")

        body_layout.addWidget(self.stats_panel)

        # ── Estado vacío ──────────────────────────────────────────
        self.empty_label = QLabel(
            "Este paciente aún no tiene ejercicios registrados.\n"
            "Inicia un ejercicio semántico para empezar a medir su progreso."
        )
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 13pt; color: #888;")
        self.empty_label.hide()
        body_layout.addWidget(self.empty_label)

        # ── Tendencia diaria ──────────────────────────────────────
        self.trend_title = QLabel("Tendencia por día")
        self.trend_title.setStyleSheet("font-size: 12pt; font-weight: 600;")
        body_layout.addWidget(self.trend_title)

        self.trend_table = self._make_table(
            ["Día", "Intentos", "Aciertos", "Precisión", "T. promedio (ms)"]
        )
        body_layout.addWidget(self.trend_table)

        # ── Últimos intentos ──────────────────────────────────────
        self.recent_title = QLabel("Últimos intentos")
        self.recent_title.setStyleSheet("font-size: 12pt; font-weight: 600;")
        body_layout.addWidget(self.recent_title)

        self.recent_table = self._make_table(
            ["Fecha y hora", "Resultado", "Tiempo (ms)"]
        )
        body_layout.addWidget(self.recent_table, 1)

        root_layout.addWidget(header_bar)
        root_layout.addWidget(body, 1)

    def _add_stat_card(self, layout, row, col, key, caption):
        card = QFrame()
        card.setObjectName("formPanel")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)

        value = QLabel("—")
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setStyleSheet("font-size: 22pt; font-weight: 700;")

        label = QLabel(caption)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 10pt; color: #888;")

        card_layout.addWidget(value)
        card_layout.addWidget(label)
        layout.addWidget(card, row, col)
        self._stat_labels[key] = value

    def _make_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        return table

    def render_report(self, patient_name, summary, recent, daily):
        self.header_title.setText(f"Progreso — {patient_name}")

        has_data = summary.get("total", 0) > 0
        self.stats_panel.setVisible(has_data)
        self.trend_title.setVisible(has_data)
        self.trend_table.setVisible(has_data)
        self.recent_title.setVisible(has_data)
        self.recent_table.setVisible(has_data)
        self.empty_label.setVisible(not has_data)

        if not has_data:
            return

        self._stat_labels["total"].setText(str(summary["total"]))
        self._stat_labels["accuracy"].setText(
            f"{summary['accuracy']:.0f}%  ({summary['correctos']}/{summary['total']})"
        )
        self._stat_labels["avg"].setText(self._fmt_ms(summary["tiempo_promedio_ms"]))
        self._stat_labels["best"].setText(self._fmt_ms(summary["mejor_tiempo_ms"]))

        self._fill_trend(daily)
        self._fill_recent(recent)

    def _fill_trend(self, daily):
        self.trend_table.setRowCount(len(daily))
        for r, d in enumerate(daily):
            self.trend_table.setItem(r, 0, QTableWidgetItem(str(d["dia"])))
            self.trend_table.setItem(r, 1, QTableWidgetItem(str(d["total"])))
            self.trend_table.setItem(r, 2, QTableWidgetItem(str(d["correctos"])))
            self.trend_table.setItem(r, 3, QTableWidgetItem(f"{d['accuracy']:.0f}%"))
            self.trend_table.setItem(
                r, 4, QTableWidgetItem(self._fmt_ms(d["tiempo_promedio_ms"]))
            )

    def _fill_recent(self, recent):
        self.recent_table.setRowCount(len(recent))
        for r, a in enumerate(recent):
            resultado = "✔ Acierto" if a["is_correct"] else "✘ Fallo"
            self.recent_table.setItem(r, 0, QTableWidgetItem(str(a["created_at"])))
            self.recent_table.setItem(r, 1, QTableWidgetItem(resultado))
            self.recent_table.setItem(
                r, 2, QTableWidgetItem(self._fmt_ms(a["reaction_time_ms"]))
            )

    @staticmethod
    def _fmt_ms(value):
        if value is None:
            return "—"
        return f"{value:.0f}"
