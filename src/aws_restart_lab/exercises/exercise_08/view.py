import random
import string

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


class PasswordGeneratorView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 8",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        subtitle = ctk.CTkLabel(
            workspace,
            text="Genera una contrasena segura ajustando sus parametros.",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=17),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, pady=(10, 22), sticky="ew")

        panel = ctk.CTkFrame(workspace, fg_color="#0f2138", corner_radius=10)
        panel.grid(row=2, column=0, sticky="ew")
        panel.grid_columnconfigure(0, weight=1)

        self.length_label = ctk.CTkLabel(
            panel,
            text="Longitud: 14",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            anchor="w",
        )
        self.length_label.grid(row=0, column=0, padx=24, pady=(22, 8), sticky="ew")

        self.length_slider = ctk.CTkSlider(panel, from_=8, to=28, number_of_steps=20, command=self._update_length)
        self.length_slider.grid(row=1, column=0, padx=24, pady=(0, 18), sticky="ew")
        self.length_slider.set(14)

        options = ctk.CTkFrame(panel, fg_color="transparent")
        options.grid(row=2, column=0, padx=24, pady=(0, 18), sticky="w")

        self.upper_var = ctk.BooleanVar(value=True)
        self.number_var = ctk.BooleanVar(value=True)
        self.symbol_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(options, text="Mayusculas", variable=self.upper_var).grid(row=0, column=0, padx=(0, 18))
        ctk.CTkCheckBox(options, text="Numeros", variable=self.number_var).grid(row=0, column=1, padx=18)
        ctk.CTkCheckBox(options, text="Simbolos", variable=self.symbol_var).grid(row=0, column=2, padx=18)

        generate_button = ctk.CTkButton(
            panel,
            text="Generar contrasena",
            height=42,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._generate,
        )
        generate_button.grid(row=3, column=0, padx=24, pady=(0, 18), sticky="ew")

        self.password_label = ctk.CTkLabel(
            panel,
            text="Presiona generar para crear una contrasena.",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            anchor="center",
        )
        self.password_label.grid(row=4, column=0, padx=24, pady=(4, 24), sticky="ew")

    def _update_length(self, value: float) -> None:
        self.length_label.configure(text=f"Longitud: {int(value)}")

    def _generate(self) -> None:
        alphabet = string.ascii_lowercase
        required = [random.choice(string.ascii_lowercase)]

        if self.upper_var.get():
            alphabet += string.ascii_uppercase
            required.append(random.choice(string.ascii_uppercase))
        if self.number_var.get():
            alphabet += string.digits
            required.append(random.choice(string.digits))
        if self.symbol_var.get():
            symbols = "!#$%&*+-=?@"
            alphabet += symbols
            required.append(random.choice(symbols))

        length = int(self.length_slider.get())
        remaining = max(0, length - len(required))
        characters = required + [random.choice(alphabet) for _ in range(remaining)]
        random.shuffle(characters)
        self.password_label.configure(text="".join(characters))
