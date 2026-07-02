from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import TodoListView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-06",
        title="Ejercicio 6",
        summary="Lista de tareas para agregar, editar, marcar y eliminar pendientes.",
        complexity="intermediate",
        factory=TodoListView,
        slot=6,
        assets_dir=Path(__file__).parent / "assets",
        tags=("todo", "tkinter"),
    )
