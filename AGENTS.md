# AGENTS.md - Contexto para Agentes de IA

## Proposito del Proyecto
Margoth es una aplicacion de escritorio 100% OFFLINE para intervencion y rehabilitacion cognitiva. La privacidad de los datos y el diseno clinico de la interfaz son prioritarios. No se permite el uso de APIs en la nube para el almacenamiento de datos de pacientes.

## Stack Tecnologico Estricto
- Lenguaje: Python 3.11+
- GUI: PyQt6
- Persistencia: SQLite3 local (Preparado para migrar a `pysqlcipher3`)
- Multimedia: Pygame (para audio sin latencia) y Pillow (procesamiento de imagenes)

## Reglas Arquitectonicas (MVC)
1. `models/`: Unica capa autorizada para ejecutar sentencias SQL y tocar la base de datos o el sistema de archivos de almacenamiento. PROHIBIDO importar `PyQt6` aqui.
2. `views/`: Unica capa autorizada para renderizar UI y manejar layouts. PROHIBIDO importar `sqlite3` o hacer queries directos. Las vistas se comunican hacia afuera emitiendo `pyqtSignal`.
3. `controllers/`: El pegamento. Reciben datos de las senales de las vistas y llaman a los metodos de los modelos.

## Reglas Clinicas de UI (Cero Sobrecarga Cognitiva)
- Cero Modales: PROHIBIDO usar `QMessageBox`, `QDialog` o ventanas emergentes. Los estados de error o los estados vacios deben renderizarse de forma inline dentro del layout actual.
- Navegacion: La aplicacion usa un patron SPA (Single Page Application) de escritorio administrado por `AppController`, inyectando las vistas centrales a traves del metodo `set_main_view()` de la `MainWindow`.
- Accesibilidad: Soporte obligatorio para hojas de estilo `.qss` (Light/Dark mode). Uso de fuentes sans-serif escalables y alto contraste. En los tableros CAA, minimizar el uso de texto si hay estimulos visuales (imagenes) presentes.

## Comandos
```bash
pip install -r requirements.txt
python src/main.py
```

## Estructura
```
src/
├── main.py                    # Entry point
├── models/                    # SQL y filesystem. Sin PyQt6.
├── views/                     # UI y layouts. Sin sqlite3.
├── controllers/               # Glue. Senales -> modelos.
└── utils/                     # Helpers (theme_manager, audio_player)
assets/styles/*.qss            # Light/Dark mode
data/margoth.db                # SQLite (gitignored)
media/{patient_uuid}/          # Multimedia por paciente
```
