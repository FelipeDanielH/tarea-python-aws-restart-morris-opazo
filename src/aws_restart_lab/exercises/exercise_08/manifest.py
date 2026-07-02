from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import PasswordGeneratorView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-08",
        title="Ejercicio 7",
        summary="Generador de contrasenas con opciones de longitud y caracteres.",
        complexity="intermediate",
        factory=PasswordGeneratorView,
        slot=7,
        assets_dir=Path(__file__).parent / "assets",
        tags=("password", "generator", "tkinter"),
    )
