# Documentación funcional — Margoth

Margoth es una aplicación de escritorio **100 % offline** para intervención y
rehabilitación cognitiva y del lenguaje. No expone ni consume ninguna API en la
nube: toda la lógica corre localmente y los datos clínicos nunca salen del
equipo. La persistencia es SQLite local y los medios se guardan en el sistema
de archivos, por paciente.

> Nota histórica: versiones muy tempranas incluían un esqueleto de API en
> Django. Se descartó por completo para cumplir el requisito de privacidad
> "100 % offline". Ya no existe backend de red.

## Módulos clínicos

### 1. Gestión de pacientes (Dashboard)
El terapeuta da de alta, edita y elimina pacientes, y sube material multimedia
personalizado (fotos y audios del entorno del paciente). Cada paciente tiene una
carpeta de medios aislada, identificada por UUID.

### 2. Tableros CAA (Comunicación Aumentativa y Alternativa)
Grillas de pictogramas/fotos con audio asociado. Al pulsar una casilla se
reproduce el audio vinculado. Pensados para pacientes con dificultades del
lenguaje expresivo.

### 3. Constructor visual de tableros CAA
Interfaz de arrastrar-asignar para montar los tableros: el terapeuta selecciona
un medio de la galería del paciente y lo coloca en una casilla de la grilla. La
configuración se guarda como `caa_boards.json` dentro de la carpeta del paciente.

### 4. Ejercicio semántico con métricas
Se muestra un estímulo visual central y tres opciones de respuesta (una correcta
y dos distractores). Se mide el tiempo de reacción con `time.perf_counter()` y se
registra cada intento (acierto/fallo + tiempo) en la tabla `exercise_metrics`.

### 5. Reportes de progreso
Vista de seguimiento por paciente que agrega `exercise_metrics`: porcentaje de
aciertos, tiempo de reacción promedio e histórico de sesiones. Es el insumo
clínico para evaluar la evolución del paciente.

## Modelo de datos (SQLite local)

| Tabla | Propósito |
|-------|-----------|
| `patients` | Datos del paciente y su carpeta de medios (UUID). |
| `patient_media` | Fotos/audios importados, con etiqueta (`label`) y tipo. |
| `exercise_metrics` | Un registro por intento de ejercicio (acierto + tiempo). |

Los tableros CAA no viven en la BD: se serializan como JSON en la carpeta de
medios de cada paciente (`caa_boards.json`).

## Principios de diseño

- **Cero sobrecarga cognitiva**: interfaces minimalistas para el paciente.
- **Cero modales**: errores y estados vacíos se renderizan inline en la vista.
- **Privacidad**: 100 % offline, datos locales.
- **Accesibilidad**: alto contraste, tipografías escalables, modo claro/oscuro.
