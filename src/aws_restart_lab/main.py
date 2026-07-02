import customtkinter as ctk

from aws_restart_lab.app import App
from aws_restart_lab.config import APPEARANCE_MODE, COLOR_THEME


def main() -> None:
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

