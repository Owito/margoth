# Margoth - Rehabilitación Cognitiva y del Lenguaje

Aplicación de escritorio 100% offline para intervención y rehabilitación cognitiva y del lenguaje. Diseñada para ofrecer una experiencia libre de sobrecarga cognitiva a los pacientes y garantizar la máxima privacidad de los datos clínicos.

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.11+ |
| **GUI** | PyQt6 (modo claro/oscuro nativo) |
| **Persistencia** | SQLite cifrado (vía pysqlcipher3) - *En desarrollo* |
| **Distribución** | PyInstaller + Inno Setup - *Planificado* |

## Arquitectura MVC

```text
margoth/
├── data/                  # Base de datos SQLite cifrada
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
│   └── utils/             # Helpers (Gestor de temas, Audio)
├── requirements.txt
└── README.md
```

## Estado del Proyecto

### Fase 1: Esqueleto MVC 
- [x] Estructura de directorios MVC
- [x] Entry point con PyQt6
- [x] Toggle dark/light mode
- [x] Estilos QSS accesibles

### Fase 2: Persistencia (Planificado) 
- [ ] Modelo de datos para pacientes
- [ ] Base SQLite cifrada
- [ ] Carga de medios (fotos/audios)

### Fase 3: Dashboard del Terapeuta (Planificado) 
- [ ] Registro de pacientes
- [ ] Carga de material multimedia
- [ ] Reportes de evolución

### Fase 4: Módulos Clínicos (Planificado) 
- [ ] Tableros CAA (Comunicación Aumentativa y Alternativa)
- [ ] Ejercicios semánticos evolutivos

## Instalación

```bash
pip install -r requirements.txt
python src/main.py
```

## Principios de Diseño

- **Cero sobrecarga cognitiva**: Interfaces minimalistas para pacientes (Teoría de Mayer)
- **Accesibilidad**: Alto contraste, tipografías escalables (Segoe UI 12pt+)
- **Privacidad**: 100% offline, datos locales cifrados
- **Personalización**: Soporte para fotos y audios del entorno del paciente

## Contribuidores

- **Carlos G** - Creador y desarrollador principal

## Licencia

MIT
