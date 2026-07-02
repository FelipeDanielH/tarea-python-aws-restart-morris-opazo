from __future__ import annotations

from importlib import import_module
from typing import Iterable

from aws_restart_lab.core.exercise import ExerciseDefinition
from aws_restart_lab.exercises.catalog import EXERCISE_MODULES


class ExerciseRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ExerciseDefinition] = {}

    def register(self, definition: ExerciseDefinition) -> None:
        if definition.slug in self._items:
            raise ValueError(f"Exercise slug already registered: {definition.slug}")
        self._items[definition.slug] = definition

    def get(self, slug: str) -> ExerciseDefinition:
        try:
            return self._items[slug]
        except KeyError as exc:
            raise KeyError(f"Unknown exercise slug: {slug}") from exc

    def list_all(self) -> list[ExerciseDefinition]:
        return list(self._items.values())

    def list_by_slots(self, total_slots: int) -> list[ExerciseDefinition | None]:
        slots: list[ExerciseDefinition | None] = [None] * total_slots
        unslotted: list[ExerciseDefinition] = []

        for definition in self._items.values():
            if definition.slot is None:
                unslotted.append(definition)
                continue

            if not 1 <= definition.slot <= total_slots:
                raise ValueError(f"Exercise slot out of range: {definition.slug} -> {definition.slot}")

            index = definition.slot - 1
            if slots[index] is not None:
                raise ValueError(f"Exercise slot already registered: {definition.slot}")
            slots[index] = definition

        for definition in unslotted:
            for index, current in enumerate(slots):
                if current is None:
                    slots[index] = definition
                    break

        return slots


def build_default_registry(modules: Iterable[str] = EXERCISE_MODULES) -> ExerciseRegistry:
    registry = ExerciseRegistry()

    for module_path in modules:
        module = import_module(module_path)
        definition = module.get_definition()
        registry.register(definition)

    return registry
