from __future__ import annotations

from typing import Callable, Protocol

import customtkinter as ctk


class RoutableScreen(Protocol):
    def grid(self, *args: object, **kwargs: object) -> object:
        ...

    def destroy(self) -> None:
        ...

    def on_show(self) -> None:
        ...

    def on_hide(self) -> None:
        ...


ScreenFactory = Callable[[ctk.CTkFrame], RoutableScreen]


class ScreenRouter:
    def __init__(self, host: ctk.CTkFrame) -> None:
        self.host = host
        self.current_screen: RoutableScreen | None = None

    def show(self, factory: ScreenFactory) -> None:
        if self.current_screen is not None:
            self.current_screen.on_hide()
            self.current_screen.destroy()

        self.current_screen = factory(self.host)
        self.current_screen.grid(row=0, column=0, sticky="nsew")
        self.current_screen.on_show()

