from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import AdditionCalculatorView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-02",
        title="Ejercicio 2",
        summary="Placeholder independiente: calculadora que solo suma dos numeros.",
        complexity="simple",
        factory=AdditionCalculatorView,
        slot=2,
        assets_dir=Path(__file__).parent / "assets",
        tags=("placeholder", "calculator"),
    )
