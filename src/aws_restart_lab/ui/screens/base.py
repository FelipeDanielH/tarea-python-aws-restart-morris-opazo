import customtkinter as ctk


class BaseScreen(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame) -> None:
        super().__init__(master, fg_color="transparent")

    def on_show(self) -> None:
        pass

    def on_hide(self) -> None:
        pass

