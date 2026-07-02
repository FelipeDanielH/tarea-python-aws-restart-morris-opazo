import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class CharacterCounterView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 2",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Escribe una frase cualquiera y calcula cuantas letras contiene.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=17),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, pady=(10, 22), sticky="ew")

        self.phrase_entry = ctk.CTkEntry(
            workspace,
            height=46,
            corner_radius=8,
            border_color="#475569",
            fg_color="#0f2138",
            text_color="#ffffff",
            placeholder_text="Ingresa una frase...",
            placeholder_text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=16),
        )
        self.phrase_entry.grid(row=2, column=0, sticky="ew")
        self.phrase_entry.bind("<Return>", lambda _event: self._count_characters())

        button = ctk.CTkButton(
            workspace,
            text="Contar caracteres",
            width=180,
            height=42,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._count_characters,
        )
        button.grid(row=3, column=0, pady=(22, 0), sticky="w")

        self.result_label = ctk.CTkLabel(
            workspace,
            text="Resultado: 0 caracteres",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            anchor="w",
        )
        self.result_label.grid(row=4, column=0, pady=(30, 8), sticky="ew")

        self.detail_label = ctk.CTkLabel(
            workspace,
            text="Tambien se muestran caracteres sin espacios.",
            text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            anchor="w",
        )
        self.detail_label.grid(row=5, column=0, sticky="ew")

    def _count_characters(self) -> None:
        phrase = self.phrase_entry.get()
        total = len(phrase)
        without_spaces = len(phrase.replace(" ", ""))
        self.result_label.configure(text=f"Resultado: {total} caracteres")
        self.detail_label.configure(text=f"Sin contar espacios: {without_spaces} caracteres")
