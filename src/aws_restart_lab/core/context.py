from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from aws_restart_lab.core.state import AppState


@dataclass(frozen=True)
class AppContext:
    state: AppState
    go_to_welcome: Callable[[], None]
    go_to_selector: Callable[[], None]
    open_exercise: Callable[[str], None]

