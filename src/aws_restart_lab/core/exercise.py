from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext


class ExerciseView(ctk.CTkFrame):
    """Base class for every exercise view mounted by the host screen."""

    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, fg_color="transparent")
        self.context = context

    def on_mount(self) -> None:
        """Called after the exercise is visible."""

    def on_unmount(self) -> None:
        """Called before the exercise is destroyed."""


ExerciseFactory = Callable[[ctk.CTkFrame, AppContext], ExerciseView]


@dataclass(frozen=True)
class ExerciseDefinition:
    slug: str
    title: str
    summary: str
    complexity: str
    factory: ExerciseFactory
    slot: int | None = None
    assets_dir: Path | None = None
    tags: tuple[str, ...] = ()

    def create_view(self, master: ctk.CTkFrame, context: AppContext) -> ExerciseView:
        return self.factory(master, context)
