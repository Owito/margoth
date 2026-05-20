# Margoth - Rehabilitación Cognitiva y del Lenguaje

Aplicación de escritorio 100% offline para intervención y rehabilitación cognitiva y del lenguaje. Diseñada para ofrecer una experiencia libre de sobrecarga cognitiva a los pacientes y garantizar la máxima privacidad de los datos clínicos.

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.11+ |
| **GUI** | PyQt6 (modo claro/oscuro nativo) |
| **Persistencia** | SQLite local (preparado para migrar a pysqlcipher3) |
| **Multimedia** | Pygame (audio in-memory) + Pillow |
| **Distribución** | PyInstaller + Inno Setup ✅ |

## Arquitectura MVC

```text
margoth/
├── data/                  # Base de datos SQLite local
├── assets/                # Estilos QSS y recursos UI
│   └── styles/
│       ├── light.qss
│       └── dark.qss
├── media/                 # Fotos y audios locales de pacientes
├── src/
│   ├── main.py            # Entry point
│   ├── models/            # Lógica de datos (BD y Cifrado)
│   ├── views/             # Componentes PyQt6
│   ├── controllers/       # Lógica de negocio
│   └── utils/             # Helpers (Gestor de temas, Audio, PathResolver)
├── build_exe.py           # Script de compilación PyInstaller
├── margoth_installer.iss  # Script de Inno Setup
├── requirements.txt
└── README.md
```

## Estado del Proyecto

### Fase 1: Esqueleto MVC ✅
- [x] Estructura de directorios MVC
- [x] Entry point con PyQt6
- [x] Toggle dark/light mode
- [x] Estilos QSS accesibles

### Fase 2: Persistencia ✅
- [x] Modelo de datos para pacientes
- [ ] Base SQLite cifrada (pysqlcipher3)
- [x] Carga de medios (fotos/audios)

### Fase 3: Dashboard del Terapeuta ✅
- [x] Registro de pacientes
- [x] Carga de material multimedia
- [x] Navegación SPA entre vistas

### Fase 4: Módulos Clínicos ✅
- [x] Tableros CAA (Comunicación Aumentativa y Alternativa)
- [x] Ejercicios semánticos evolutivos

### Fase 5: Gestor de Medios Locales ✅
- [x] Importación segura de medios por paciente
- [x] Registro de medios en SQLite

### Fase 6: Constructor Visual de Tableros CAA ✅
- [x] Interfaz de asignación de medios a grilla 2x2
- [x] Persistencia de configuración en `caa_boards.json`
- [x] Navegación limpia desde Dashboard

### Fase 7: Ejercicios Semánticos con Métricas ✅
- [x] Estímulo visual central con 3 opciones de respuesta
- [x] Medición de tiempo de reacción con `time.perf_counter()`
- [x] Registro de aciertos/fallos en tabla `exercise_metrics`

### Fase 8: Empaquetado y Distribución ✅
- [x] Helper de rutas `PathResolver` para modo dev/compilado
- [x] Script de build PyInstaller (`build_exe.py`)
- [x] Script de Inno Setup (`margoth_installer.iss`)
- [x] Verificación de creación de `data/` y `media/` junto al binario

## Instalación y Desarrollo

### Ejecución local
```bash
pip install -r requirements.txt
python src/main.py
```

### Compilación (Windows)
```bash
pip install pyinstaller
python build_exe.py
```
El ejecutable se generará en `dist/Margoth/`.

### Creación del instalador
1. Instalar [Inno Setup](https://jrsoftware.org/isdl.php).
2. Abrir `margoth_installer.iss` en Inno Setup.
3. Compilar para obtener `dist/Margoth_Setup.exe`.

## Principios de Diseño

- **Cero sobrecarga cognitiva**: Interfaces minimalistas para pacientes (Teoría de Mayer)
- **Accesibilidad**: Alto contraste, tipografías escalables (Segoe UI 12pt+)
- **Privacidad**: 100% offline, datos locales cifrados
- **Personalización**: Soporte para fotos y audios del entorno del paciente

## Contribuidores

- **Carlos G** - Creador y desarrollador principal

## Licencia

MIT
