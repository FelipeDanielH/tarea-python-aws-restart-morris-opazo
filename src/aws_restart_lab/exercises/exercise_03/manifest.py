from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import FileNamePickerView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-03",
        title="Ejercicio 3",
        summary="Placeholder independiente: selecciona un archivo y muestra su nombre.",
        complexity="simple",
        factory=FileNamePickerView,
        slot=3,
        assets_dir=Path(__file__).parent / "assets",
        tags=("placeholder", "file-dialog"),
    )
