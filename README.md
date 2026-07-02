# AWS re/Start - Laboratorio

Contenedor de ejercicios hecho con Python y CustomTkinter.

El objetivo de esta primera etapa es dejar una arquitectura limpia para:

- mostrar una pantalla de bienvenida y guardar el nombre del estudiante;
- mostrar un selector de ejercicios;
- montar ejercicios simples como una vista pequena;
- montar ejercicios complejos como paquetes propios con assets, dominio, servicios y vistas internas.

La capa visual queda intencionalmente simple por ahora. El diseno se puede trabajar despues sin mover la base del proyecto.

## Requisitos

- Python 3.10 o superior
- CustomTkinter

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Tambien puedes instalar solo dependencias con:

```powershell
python -m pip install -r requirements.txt
```

## Ejecutar

```powershell
python -m aws_restart_lab
```

o, si instalaste el paquete en modo editable:

```powershell
aws-restart-lab
```

## Estructura principal

```text
src/aws_restart_lab/
  app.py                    # Ventana principal y flujo entre pantallas
  main.py                   # Punto de entrada
  config.py                 # Constantes generales
  core/
    context.py              # Acciones y estado compartidos con pantallas/ejercicios
    exercise.py             # Contratos base de ejercicios
    registry.py             # Registro de ejercicios disponibles
    router.py               # Cambio de pantallas
    state.py                # Estado de sesion
  ui/screens/
    welcome.py              # Pantalla para ingresar nombre
    exercise_selector.py    # Selector de ejercicios
    exercise_host.py        # Contenedor para ejecutar un ejercicio
  exercises/
    catalog.py              # Lista explicita de ejercicios cargados
    exercise_01/            # Ejercicio simple de ejemplo
```
