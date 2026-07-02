from __future__ import annotations

import tkinter as tk
from collections.abc import Callable

from .entities import Direction


class InputHandler:
    def __init__(
        self,
        widget: tk.Misc,
        on_direction: Callable[[Direction], None],
        on_toggle_running: Callable[[], None] | None = None,
    ) -> None:
        self.widget = widget
        self.on_direction = on_direction
        self.on_toggle_running = on_toggle_running
        self._bindings: dict[str, str] = {}

    def bind(self) -> None:
        key_map = {
            "<Up>": Direction.NE,
            "<Right>": Direction.SE,
            "<Down>": Direction.SW,
            "<Left>": Direction.NW,
            "w": Direction.NE,
            "d": Direction.SE,
            "s": Direction.SW,
            "a": Direction.NW,
        }
        for sequence, direction in key_map.items():
            bind_id = self.widget.bind(sequence, lambda _event, value=direction: self.on_direction(value), add="+")
            self._bindings[sequence] = bind_id
        if self.on_toggle_running is not None:
            bind_id = self.widget.bind("<space>", lambda _event: self.on_toggle_running(), add="+")
            self._bindings["<space>"] = bind_id

    def unbind(self) -> None:
        for sequence in self._bindings:
            self.widget.unbind(sequence)
        self._bindings.clear()
