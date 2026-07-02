from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import ScientificCalculatorView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-05",
        title="Ejercicio 5",
        summary="Calculadora casi cientifica construida con CustomTkinter.",
        complexity="intermediate",
        factory=ScientificCalculatorView,
        slot=5,
        assets_dir=Path(__file__).parent / "assets",
        tags=("calculator", "scientific"),
    )
