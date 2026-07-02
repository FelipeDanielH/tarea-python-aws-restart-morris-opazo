import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class CenteredDiamondView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=0)
        workspace.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 3",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, columnspan=2, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Ingresa un numero y genera un rombo centrado con asteriscos.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=17),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=(10, 22), sticky="ew")

        control_panel = ctk.CTkFrame(workspace, fg_color="#0f2138", corner_radius=10)
        control_panel.grid(row=2, column=0, sticky="nw", padx=(0, 22))
        control_panel.grid_columnconfigure(0, weight=1)

        self.size_entry = ctk.CTkEntry(
            control_panel,
            width=180,
            height=42,
            corner_radius=8,
            border_color="#475569",
            fg_color="#0a192c",
            text_color="#ffffff",
            placeholder_text="Numero",
            placeholder_text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=15),
        )
        self.size_entry.grid(row=0, column=0, padx=22, pady=(22, 14), sticky="ew")
        self.size_entry.insert(0, "4")
        self.size_entry.bind("<Return>", lambda _event: self._draw_diamond())

        button = ctk.CTkButton(
            control_panel,
            text="Dibujar rombo",
            height=42,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._draw_diamond,
        )
        button.grid(row=1, column=0, padx=22, pady=(0, 22), sticky="ew")

        output = ctk.CTkFrame(workspace, fg_color="#081526", corner_radius=10, border_color="#334155", border_width=1)
        output.grid(row=2, column=1, sticky="nsew")
        output.grid_columnconfigure(0, weight=1)

        self.diamond_label = ctk.CTkLabel(
            output,
            text="",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            justify="center",
        )
        self.diamond_label.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")

        self._draw_diamond()

    def _draw_diamond(self) -> None:
        try:
            size = int(self.size_entry.get())
        except ValueError:
            self.diamond_label.configure(text="Ingresa un numero valido.")
            return

        if size < 1:
            self.diamond_label.configure(text="El numero debe ser mayor a cero.")
            return
        if size > 18:
            self.diamond_label.configure(text="Usa un numero de 18 o menor.")
            return

        lines = []
        for level in range(1, size + 1):
            lines.append(" " * (size - level) + "*" * level)
        for level in range(size - 1, 0, -1):
            lines.append(" " * (size - level) + "*" * level)

        self.diamond_label.configure(text="\n".join(lines))
