# AWS re/Start - Laboratorio de Python

Aplicacion de escritorio hecha con Python y CustomTkinter para reunir ejercicios en una sola interfaz. Incluye una pantalla de bienvenida, un selector por pestanas y ejercicios independientes, desde formularios simples hasta un juego isometrico con Canvas y assets.

## Inicio rapido

Solo necesitas tener Python 3.10 o superior instalado.

### Windows

Opcion recomendada:

```bat
run.bat
```

Tambien puedes ejecutarlo desde PowerShell:

```powershell
.\run.ps1
```

Si PowerShell bloquea el script por permisos, usa:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

### macOS o Linux

```bash
chmod +x run.sh
./run.sh
```

## Que hacen los scripts

Los scripts de ejecucion preparan todo automaticamente:

1. Crean el entorno virtual `.venv` si no existe.
2. Instalan las dependencias desde `requirements.txt`.
3. Configuran la ruta del proyecto.
4. Abren la aplicacion.

No necesitas activar el entorno virtual manualmente para usar la app con estos scripts.

## Ejercicios incluidos

| Pestana | Ejercicio |
| --- | --- |
| Ejercicio 1 | Formulario para imprimir nombre, apellido, edad y dato extra |
| Ejercicio 2 | Conteo de caracteres de una frase |
| Ejercicio 3 | Rombo centrado generado con asteriscos |
| Ejercicio 4 | Calculadora de suma, resta, multiplicacion y division |
| Ejercicio 5 | Calculadora casi cientifica |
| Ejercicio 6 | Lista de tareas con agregar, editar, marcar y eliminar |
| Ejercicio 7 | Generador de contrasenas |
| Ejercicio 8 | Juego Snake isometrico con Canvas y assets |

## Ejecucion manual

Si prefieres hacerlo paso a paso:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
python -m aws_restart_lab
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
PYTHONPATH=src python -m aws_restart_lab
```

## Estructura del proyecto

```text
.
  run.bat                  # Arranque rapido para Windows
  run.ps1                  # Arranque rapido para PowerShell
  run.sh                   # Arranque rapido para macOS/Linux
  requirements.txt         # Dependencias principales
  src/aws_restart_lab/
    app.py                 # Ventana principal y flujo de pantallas
    main.py                # Punto de entrada
    core/                  # Registro, estado, router y contratos base
    ui/screens/            # Bienvenida y selector de ejercicios
    exercises/             # Cada ejercicio vive en su propia carpeta
```

## Nota

La aplicacion abre en pantalla completa. Presiona `Esc` para salir del modo fullscreen durante pruebas.
