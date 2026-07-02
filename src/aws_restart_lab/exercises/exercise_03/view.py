from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class FileNamePickerView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 3",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Selecciona un archivo para mostrar su nombre.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=18),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, pady=(16, 22), sticky="ew")

        button = ctk.CTkButton(
            workspace,
            text="Elegir archivo",
            width=170,
            height=40,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._choose_file,
        )
        button.grid(row=2, column=0, sticky="w")

        self.file_label = ctk.CTkLabel(
            workspace,
            text="Archivo: ninguno",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            anchor="w",
        )
        self.file_label.grid(row=3, column=0, pady=(24, 0), sticky="ew")

    def _choose_file(self) -> None:
        selected_path = filedialog.askopenfilename(title="Selecciona un archivo")
        if not selected_path:
            return

        self.file_label.configure(text=f"Archivo: {Path(selected_path).name}")

