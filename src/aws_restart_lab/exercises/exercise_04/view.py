import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class BasicOperationsView(ExerciseView):
    OPERATIONS = ("Suma", "Resta", "Multiplicacion", "Division")

    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 4",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Elige una operacion y calcula el resultado de dos valores.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=17),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, pady=(10, 22), sticky="ew")

        panel = ctk.CTkFrame(workspace, fg_color="#0f2138", corner_radius=10)
        panel.grid(row=2, column=0, sticky="ew")
        panel.grid_columnconfigure((0, 1, 2), weight=1)

        self.first_entry = self._number_entry(panel, "Valor 1")
        self.first_entry.grid(row=0, column=0, padx=(22, 10), pady=(22, 14), sticky="ew")

        self.operation_menu = ctk.CTkOptionMenu(
            panel,
            values=list(self.OPERATIONS),
            fg_color="#081526",
            button_color="#ff9900",
            button_hover_color="#e88900",
            dropdown_fg_color="#0f2138",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=15),
        )
        self.operation_menu.grid(row=0, column=1, padx=10, pady=(22, 14), sticky="ew")
        self.operation_menu.set("Suma")

        self.second_entry = self._number_entry(panel, "Valor 2")
        self.second_entry.grid(row=0, column=2, padx=(10, 22), pady=(22, 14), sticky="ew")

        button = ctk.CTkButton(
            panel,
            text="Calcular",
            height=42,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._calculate,
        )
        button.grid(row=1, column=0, padx=22, pady=(6, 22), sticky="ew")

        self.result_label = ctk.CTkLabel(
            panel,
            text="Resultado: -",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        self.result_label.grid(row=1, column=1, columnspan=2, padx=(10, 22), pady=(6, 22), sticky="ew")

    def _number_entry(self, master: ctk.CTkFrame, placeholder: str) -> ctk.CTkEntry:
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

    def _calculate(self) -> None:
        try:
            first = float(self.first_entry.get().replace(",", "."))
            second = float(self.second_entry.get().replace(",", "."))
        except ValueError:
            self.result_label.configure(text="Resultado: valores invalidos")
            return

        operation = self.operation_menu.get()
        if operation == "Suma":
            result = first + second
        elif operation == "Resta":
            result = first - second
        elif operation == "Multiplicacion":
            result = first * second
        else:
            if second == 0:
                self.result_label.configure(text="Resultado: no se puede dividir por cero")
                return
            result = first / second

        self.result_label.configure(text=f"Resultado: {self._format_number(result)}")

    def _format_number(self, value: float) -> str:
        if value.is_integer():
            return str(int(value))
        return f"{value:.4f}".rstrip("0").rstrip(".")
