# Agregar ejercicios

La aplicacion carga ejercicios desde `src/aws_restart_lab/exercises/catalog.py`.
Cada ejercicio debe exponer una funcion `get_definition()` en un modulo `manifest.py`.

## Ejercicio simple

Usa esta forma cuando el ejercicio solo necesita una vista y algo de logica local:

```text
src/aws_restart_lab/exercises/mi_ejercicio/
  __init__.py
  manifest.py
  view.py
  assets/
    .gitkeep
```

`manifest.py` devuelve un `ExerciseDefinition`:

```python
from aws_restart_lab.core.exercise import ExerciseDefinition
from .view import MiEjercicioView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="mi-ejercicio",
        title="Mi ejercicio",
        summary="Descripcion corta para el selector.",
        complexity="simple",
        factory=MiEjercicioView,
    )
```

Luego agrega el modulo al catalogo:

```python
EXERCISE_MODULES = (
    "aws_restart_lab.exercises.exercise_01.manifest",
    "aws_restart_lab.exercises.mi_ejercicio.manifest",
)
```

## Proyecto complejo

Para un ejercicio grande, como un juego isometrico, mantenlo encapsulado en su propio paquete:

```text
src/aws_restart_lab/exercises/juego_isometrico/
  __init__.py
  manifest.py
  assets/
    sprites/
    tiles/
    audio/
  domain/
    __init__.py
  services/
    __init__.py
  systems/
    __init__.py
  ui/
    __init__.py
    game_view.py
```

La aplicacion principal solo necesita conocer el `manifest.py`. Todo lo demas puede crecer dentro del paquete sin cambiar el router, el selector o las otras pantallas.

Hay un template de carpetas en:

```text
src/aws_restart_lab/exercises/_complex_template/
```

Ese template no se carga en la aplicacion. Sirve solo como punto de partida para copiar o replicar la estructura de un proyecto grande.

## Contrato de vistas

La vista principal de un ejercicio debe heredar de `ExerciseView`.
Puede usar estos hooks:

- `on_mount()`: se ejecuta cuando el ejercicio queda visible.
- `on_unmount()`: se ejecuta antes de desmontarlo.

Estos hooks son utiles para iniciar o detener timers, loops, sonidos, cargas de assets o conexiones internas.
