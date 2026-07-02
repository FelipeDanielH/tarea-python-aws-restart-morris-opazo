from collections.abc import Callable

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseDefinition, ExerciseView
from aws_restart_lab.ui.screens.base import BaseScreen


class ExerciseHostScreen(BaseScreen):
    def __init__(
        self,
        master: ctk.CTkFrame,
        context: AppContext,
        exercise: ExerciseDefinition,
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self.exercise_view: ExerciseView | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=32, pady=(24, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text=exercise.title,
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        back_button = ctk.CTkButton(header, text="Volver", width=96, command=on_back)
        back_button.grid(row=0, column=1, padx=(16, 0), sticky="e")

        body = ctk.CTkFrame(self)
        body.grid(row=1, column=0, padx=32, pady=(0, 32), sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.exercise_view = exercise.create_view(body, context)
        self.exercise_view.grid(row=0, column=0, sticky="nsew")

    def on_show(self) -> None:
        if self.exercise_view is not None:
            self.exercise_view.on_mount()

    def on_hide(self) -> None:
        if self.exercise_view is not None:
            self.exercise_view.on_unmount()

