from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .src.app import SnakeGameApp


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-07",
        title="Ejercicio 7",
        summary="Juego inventado: Snake isometrico con Canvas, niveles, marines y assets.",
        complexity="complex",
        factory=SnakeGameApp,
        slot=7,
        assets_dir=Path(__file__).parent / "assets",
        tags=("game", "snake", "isometric"),
    )
