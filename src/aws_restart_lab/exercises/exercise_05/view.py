import math

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class ScientificCalculatorView(ExerciseView):
    BUTTON_WIDTH = 74
    BUTTON_HEIGHT = 42

    SAFE_NAMES = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "pow": pow,
    }

    BUTTONS = (
        ("7", "8", "9", "/", "sqrt("),
        ("4", "5", "6", "*", "sin("),
        ("1", "2", "3", "-", "cos("),
        ("0", ".", "(", ")", "+"),
        ("pi", "e", "**", "log(", "ln("),
    )

    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 5",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="center",
        )
        title.grid(row=0, column=0, sticky="ew")

        content = ctk.CTkFrame(workspace, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(content, fg_color="#0f2138", corner_radius=10)
        panel.grid(row=0, column=0, sticky="")
        for column in range(5):
            panel.grid_columnconfigure(column, weight=1, minsize=self.BUTTON_WIDTH, uniform="calculator")

        self.expression_entry = ctk.CTkEntry(
            panel,
            width=430,
            height=50,
            corner_radius=8,
            border_color="#475569",
            fg_color="#081526",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Consolas", size=20),
            justify="right",
        )
        self.expression_entry.grid(row=0, column=0, columnspan=5, padx=18, pady=(18, 12), sticky="ew")
        self.expression_entry.bind("<Return>", lambda _event: self._evaluate())

        self.result_label = ctk.CTkLabel(
            panel,
            text="Resultado: -",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            anchor="e",
        )
        self.result_label.grid(row=1, column=0, columnspan=5, padx=18, pady=(0, 12), sticky="ew")

        for row_index, row in enumerate(self.BUTTONS, start=2):
            for column_index, label in enumerate(row):
                button = ctk.CTkButton(
                    panel,
                    text=label,
                    width=self.BUTTON_WIDTH,
                    height=self.BUTTON_HEIGHT,
                    fg_color="#132a46",
                    hover_color="#1d3a5d",
                    text_color="#ffffff",
                    font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                    command=lambda value=label: self._append(value),
                )
                button.grid(row=row_index, column=column_index, padx=6, pady=6, sticky="ew")

        clear_button = ctk.CTkButton(
            panel,
            text="Limpiar",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="#334155",
            hover_color="#475569",
            command=self._clear,
        )
        clear_button.grid(row=7, column=0, columnspan=2, padx=6, pady=(10, 18), sticky="ew")

        delete_button = ctk.CTkButton(
            panel,
            text="Borrar",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="#334155",
            hover_color="#475569",
            command=self._delete_last,
        )
        delete_button.grid(row=7, column=2, padx=6, pady=(10, 18), sticky="ew")

        equals_button = ctk.CTkButton(
            panel,
            text="=",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            command=self._evaluate,
        )
        equals_button.grid(row=7, column=3, columnspan=2, padx=6, pady=(10, 18), sticky="ew")

    def _append(self, value: str) -> None:
        self.expression_entry.insert("end", value)

    def _clear(self) -> None:
        self.expression_entry.delete(0, "end")
        self.result_label.configure(text="Resultado: -")

    def _delete_last(self) -> None:
        text = self.expression_entry.get()
        self.expression_entry.delete(0, "end")
        self.expression_entry.insert(0, text[:-1])

    def _evaluate(self) -> None:
        expression = self.expression_entry.get().strip()
        if not expression:
            self.result_label.configure(text="Resultado: -")
            return

        try:
            result = eval(expression, {"__builtins__": {}}, self.SAFE_NAMES)
        except Exception:
            self.result_label.configure(text="Resultado: expresion invalida")
            return

        if isinstance(result, float) and result.is_integer():
            result_text = str(int(result))
        elif isinstance(result, float):
            result_text = f"{result:.8f}".rstrip("0").rstrip(".")
        else:
            result_text = str(result)
        self.result_label.configure(text=f"Resultado: {result_text}")
