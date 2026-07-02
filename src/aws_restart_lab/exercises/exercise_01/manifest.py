from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import ExerciseOneView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-01",
        title="Ejercicio 1",
        summary="Formulario que imprime nombre, apellido, edad y un dato extra.",
        complexity="simple",
        factory=ExerciseOneView,
        slot=1,
        assets_dir=Path(__file__).parent / "assets",
        tags=("button", "message"),
    )
