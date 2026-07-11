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
- [x] Validación de ejecución del ejecutable compilado (`Margoth.exe`)

### Fase 9: Medios etiquetados ✅
- [x] Columna `label` en `patient_media` (con migración idempotente)
- [x] El ejercicio semántico usa etiquetas legibles, no el nombre de archivo
- [x] Campo de etiqueta al subir un medio

### Fase 10: Reportes y gestión de pacientes ✅
- [x] Vista de reportes de progreso (aciertos, tiempos, tendencia diaria)
- [x] Editar y eliminar pacientes (borrado en cascada de medios y métricas)

### Fase 11: Tableros CAA múltiples ✅
- [x] Varios tableros por paciente (upsert por id, sin sobrescribir)
- [x] Tamaño de grilla configurable (1..4 × 1..4)
- [x] Selector de tablero en el constructor y en el visor

### Calidad ✅
- [x] Suite de pruebas de la capa de modelos (`pytest`, 44 tests)
- [x] Integración continua en GitHub Actions
- [x] Ícono propio de la aplicación (`assets/icon.ico`)

## Verificación del Ejecutable Compilado

Tras ejecutar `Margoth.exe` en `dist/Margoth/`:
```
dist/Margoth/
├── data/
│   └── margoth.db          # BD creada automáticamente
├── media/                  # Carpeta lista para multimedia
├── _internal/              # Dependencias empaquetadas
└── Margoth.exe             # Binario aislado
```
El `PathResolver` confirma que las rutas se resuelven correctamente usando `sys.executable` como base en modo frozen.

## Instalación (usuario final)

Estas instrucciones son para el terapeuta que va a usar la aplicación. **No
necesitas instalar Python ni tener conexión a internet.**

**Requisitos:** Windows 10 u 11 (64 bits).

### Pasos

1. Consigue el archivo **`Margoth_Setup.exe`** (te lo entrega quien distribuye la
   aplicación).
2. Haz doble clic en `Margoth_Setup.exe`.
3. Si Windows muestra el aviso azul *"Windows protegió tu PC"*, haz clic en
   **"Más información"** y luego en **"Ejecutar de todas formas"**.
   > Este aviso no aparece si antes se instaló en el equipo el certificado de
   > confianza de Margoth (ver *Firma de código* en la sección de Desarrollo).
   > En una implementación gestionada, quien instala la app ya lo dejó listo.
4. Sigue el asistente y pulsa *Instalar*. **No pide permisos de administrador**:
   se instala en tu carpeta de usuario.
5. Al terminar, abre **Margoth** desde el acceso directo del **Escritorio** o
   del **menú Inicio**.

La primera vez que la abras, la aplicación crea sola sus carpetas de datos; no
tienes que configurar nada.

### Dónde quedan tus datos

Todo se guarda **en tu equipo**, en:

```
C:\Users\<tu-usuario>\AppData\Local\Margoth\
├── data\margoth.db     # base de datos (pacientes, métricas)
└── media\              # fotos y audios de cada paciente
```

> **Respaldo:** para tener una copia de seguridad, copia esa carpeta `Margoth`
> a un disco externo o a la nube de tu preferencia.

### Actualizar

Ejecuta la versión nueva de `Margoth_Setup.exe`. Se instala sobre la anterior y
**conserva tus datos**.

### Desinstalar

Abre *Configuración → Aplicaciones → Margoth → Desinstalar* (o usa el acceso de
desinstalación del menú Inicio).

> Al desinstalar, **tus datos (`data\` y `media\`) NO se borran** a propósito,
> para no perder información clínica. Si además quieres eliminarlos, borra a mano
> la carpeta `C:\Users\<tu-usuario>\AppData\Local\Margoth`.

## Desarrollo

### Ejecución local
```bash
pip install -r requirements.txt
python src/main.py
```

### Pruebas
```bash
pip install -r requirements-dev.txt
pytest
```
La capa de modelos se prueba headless (sin PyQt6). El mismo comando corre en
CI (GitHub Actions) en cada push y pull request.

### Regenerar el ícono
```bash
python tools/generate_icon.py   # -> assets/icon.png y assets/icon.ico
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

### Firma de código (equipos internos)

La app y el instalador se firman con un certificado **auto-firmado**. Esto
sirve para distribución interna (equipos que tú controlas): tras confiar el
certificado en cada equipo, la firma es válida y desaparece el "Editor
desconocido".

> ⚠️ Un certificado auto-firmado **no** elimina SmartScreen para usuarios
> externos/públicos. Para eso se necesita un certificado **EV** comprado
> (~US$300-600/año, con token). El pipeline de abajo funciona igual con un
> cert comprado: solo cambia el certificado usado.

**Preparación (una sola vez, en el equipo de build):**
```powershell
# Crea el certificado y exporta signing\Margoth-CodeSigning.{cer,pfx}
tools\New-CodeSigningCert.ps1 -PfxPassword "<una-contraseña>"
```
El `.pfx` (clave privada) es tu respaldo: guárdalo a salvo, **nunca lo subas**
(la carpeta `signing/` está en `.gitignore`).

**En cada release:**
```powershell
python build_exe.py            # 1. genera dist\Margoth\
tools\sign.ps1 -AppOnly        # 2. firma Margoth.exe
ISCC margoth_installer.iss     # 3. empaqueta el .exe ya firmado
tools\sign.ps1 -InstallerOnly  # 4. firma Margoth_Setup.exe
```
Ambas firmas incluyen sello de tiempo RFC3161 (siguen válidas tras expirar el
certificado).

**En cada equipo donde se instale Margoth (una vez):**
```powershell
# Reparte signing\Margoth-CodeSigning.cer (es público) y ejecútalo allí:
tools\Trust-MargothCert.ps1
```
Windows pedirá confirmar la instalación del certificado raíz (es normal).
Después, `Margoth_Setup.exe` mostrará al editor **Carlos G** como válido.

## Principios de Diseño

- **Cero sobrecarga cognitiva**: Interfaces minimalistas para pacientes (Teoría de Mayer)
- **Accesibilidad**: Alto contraste, tipografías escalables (Segoe UI 12pt+)
- **Privacidad**: 100% offline. Los datos clínicos nunca salen del equipo (ver *Seguridad y privacidad*)
- **Personalización**: Soporte para fotos y audios del entorno del paciente

## Seguridad y privacidad

- **Sin nube**: la aplicación no consume ni expone ninguna API de red. Todos
  los datos (BD SQLite y medios) viven en el equipo del terapeuta.
- **Aislamiento por paciente**: los medios se guardan en carpetas separadas
  identificadas por UUID.
- **Cifrado en reposo (pendiente)**: hoy la base de datos SQLite **no** está
  cifrada. La migración a [SQLCipher](https://www.zetetic.net/sqlcipher/)
  (vía `pysqlcipher3`) está planificada como mejora futura; se difirió porque
  requiere binarios nativos que complican el empaquetado con PyInstaller en
  Windows. Mientras tanto, la protección recae en el control de acceso del
  sistema operativo. **No usar en un equipo compartido sin cuenta de usuario
  protegida.**

## Contribuidores

- **Carlos G** - Creador y desarrollador principal

## Licencia

MIT
