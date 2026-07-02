from dataclasses import dataclass


@dataclass
class AppState:
    user_name: str = ""
    selected_exercise_slug: str | None = None

