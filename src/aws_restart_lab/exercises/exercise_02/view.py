import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class AdditionCalculatorView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=0)
        workspace.grid_columnconfigure(1, weight=0)
        workspace.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 2",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, columnspan=3, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Calculadora placeholder: solo suma.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=18),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, columnspan=3, pady=(16, 20), sticky="ew")

        self.first_entry = self._number_entry(workspace, "Primer numero")
        self.first_entry.grid(row=2, column=0, sticky="w")

        plus = ctk.CTkLabel(
            workspace,
            text="+",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
        )
        plus.grid(row=2, column=1, padx=16)

        self.second_entry = self._number_entry(workspace, "Segundo numero")
        self.second_entry.grid(row=2, column=2, sticky="w")

        calculate_button = ctk.CTkButton(
            workspace,
            text="Sumar",
            width=140,
            height=40,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._calculate,
        )
        calculate_button.grid(row=3, column=0, pady=(24, 0), sticky="w")

        self.result_label = ctk.CTkLabel(
            workspace,
            text="Resultado: -",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            anchor="w",
        )
        self.result_label.grid(row=4, column=0, columnspan=3, pady=(24, 0), sticky="ew")

    def _number_entry(self, master: ctk.CTkFrame, placeholder: str) -> ctk.CTkEntry:
        return ctk.CTkEntry(
            master,
            width=190,
            height=42,
            corner_radius=8,
            border_color="#475569",
            fg_color="#0f2138",
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
            self.result_label.configure(text="Resultado: ingresa dos numeros validos")
            return

        result = first + second
        if result.is_integer():
            result_text = str(int(result))
        else:
            result_text = f"{result:.2f}".rstrip("0").rstrip(".")
        self.result_label.configure(text=f"Resultado: {result_text}")

