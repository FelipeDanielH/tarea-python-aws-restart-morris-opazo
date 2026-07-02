from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import BasicOperationsView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-04",
        title="Ejercicio 4",
        summary="Calculadora de dos valores con suma, resta, multiplicacion y division.",
        complexity="simple",
        factory=BasicOperationsView,
        slot=4,
        assets_dir=Path(__file__).parent / "assets",
        tags=("calculator", "operations"),
    )
