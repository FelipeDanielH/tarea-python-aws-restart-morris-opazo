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
        workspace.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 1",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, columnspan=2, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Ingresa tus datos y presiona imprimir.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=17),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=(10, 24), sticky="ew")

        form = ctk.CTkFrame(workspace, fg_color="#0f2138", corner_radius=10)
        form.grid(row=2, column=0, sticky="nsew", padx=(0, 18))
        form.grid_columnconfigure(0, weight=1)

        self.name_entry = self._entry(form, "Nombre")
        self.name_entry.grid(row=0, column=0, padx=22, pady=(22, 12), sticky="ew")
        self.lastname_entry = self._entry(form, "Apellido")
        self.lastname_entry.grid(row=1, column=0, padx=22, pady=12, sticky="ew")
        self.age_entry = self._entry(form, "Edad")
        self.age_entry.grid(row=2, column=0, padx=22, pady=12, sticky="ew")
        self.extra_entry = self._entry(form, "Dato extra")
        self.extra_entry.grid(row=3, column=0, padx=22, pady=12, sticky="ew")

        button = ctk.CTkButton(
            form,
            text="Imprimir datos",
            height=42,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._print_data,
        )
        button.grid(row=4, column=0, padx=22, pady=(14, 22), sticky="ew")

        output = ctk.CTkFrame(workspace, fg_color="#081526", corner_radius=10, border_color="#334155", border_width=1)
        output.grid(row=2, column=1, sticky="nsew")
        output.grid_columnconfigure(0, weight=1)

        output_title = ctk.CTkLabel(
            output,
            text="Datos ingresados",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            anchor="w",
        )
        output_title.grid(row=0, column=0, padx=24, pady=(24, 10), sticky="ew")

        self.output_label = ctk.CTkLabel(
            output,
            text="Aun no hay datos para mostrar.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Consolas", size=17),
            anchor="nw",
            justify="left",
        )
        self.output_label.grid(row=1, column=0, padx=24, pady=(8, 24), sticky="nsew")

    def _entry(self, master: ctk.CTkFrame, placeholder: str) -> ctk.CTkEntry:
        return ctk.CTkEntry(
            master,
            height=42,
            corner_radius=8,
            border_color="#475569",
            fg_color="#0a192c",
            text_color="#ffffff",
            placeholder_text=placeholder,
            placeholder_text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=15),
        )

    def _print_data(self) -> None:
        name = self.name_entry.get().strip() or "Sin nombre"
        lastname = self.lastname_entry.get().strip() or "Sin apellido"
        age = self.age_entry.get().strip() or "Sin edad"
        extra = self.extra_entry.get().strip() or "Sin dato extra"

        self.output_label.configure(
            text=(
                f"Nombre:   {name}\n"
                f"Apellido: {lastname}\n"
                f"Edad:     {age}\n"
                f"Extra:    {extra}"
            )
        )
