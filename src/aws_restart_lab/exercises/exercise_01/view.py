import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class ExerciseOneView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 1",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        self.output_label = ctk.CTkLabel(
            workspace,
            text="Presiona el boton para mostrar el mensaje.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=18),
            anchor="w",
        )
        self.output_label.grid(row=1, column=0, pady=(18, 22), sticky="ew")

        button = ctk.CTkButton(
            workspace,
            text="Decir hola",
            width=160,
            height=40,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._say_hello,
        )
        button.grid(row=2, column=0, sticky="w")

    def _say_hello(self) -> None:
        self.output_label.configure(text="Hola mundo")
