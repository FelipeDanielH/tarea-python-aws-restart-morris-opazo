from pathlib import Path

from aws_restart_lab.core.exercise import ExerciseDefinition

from .view import CharacterCounterView


def get_definition() -> ExerciseDefinition:
    return ExerciseDefinition(
        slug="exercise-02",
        title="Ejercicio 2",
        summary="Funcion que cuenta los caracteres de una frase ingresada.",
        complexity="simple",
        factory=CharacterCounterView,
        slot=2,
        assets_dir=Path(__file__).parent / "assets",
        tags=("text", "counter"),
    )
