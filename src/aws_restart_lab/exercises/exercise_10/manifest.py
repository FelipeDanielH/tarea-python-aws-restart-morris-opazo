from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .src.app import SnakeGameApp


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-10",
        title="Ejercicio 10",
        summary="Juego Snake isometrico con Canvas, arquitectura modular y assets preparados.",
        complexity="complex",
        factory=SnakeGameApp,
        slot=10,
        assets_dir=Path(__file__).parent / "assets",
        tags=("game", "snake", "isometric"),
    )

