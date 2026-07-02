from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import CenteredDiamondView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-03",
        title="Ejercicio 3",
        summary="Dibuja un rombo centrado a partir de un numero ingresado.",
        complexity="simple",
        factory=CenteredDiamondView,
        slot=3,
        assets_dir=Path(__file__).parent / "assets",
        tags=("pattern", "diamond"),
    )
