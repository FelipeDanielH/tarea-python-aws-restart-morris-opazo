import customtkinter as ctk

from aws_restart_lab.config import APP_TITLE, DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE
from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.registry import build_default_registry
from aws_restart_lab.core.router import ScreenRouter
from aws_restart_lab.core.state import AppState
from aws_restart_lab.ui.screens.exercise_host import ExerciseHostScreen
from aws_restart_lab.ui.screens.exercise_selector import ExerciseSelectorScreen
from aws_restart_lab.ui.screens.welcome import WelcomeScreen


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(DEFAULT_WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.app_state = AppState()
        self.registry = build_default_registry()

        self.screen_host = ctk.CTkFrame(self, fg_color="transparent")
        self.screen_host.grid(row=0, column=0, sticky="nsew")
        self.screen_host.grid_columnconfigure(0, weight=1)
        self.screen_host.grid_rowconfigure(0, weight=1)

        self.router = ScreenRouter(self.screen_host)
        self.context = AppContext(
            state=self.app_state,
            go_to_welcome=self.show_welcome,
            go_to_selector=self.show_selector,
            open_exercise=self.show_exercise,
        )

        self.show_welcome()

    def show_welcome(self) -> None:
        self.title("Ejercicios App")
        self.router.show(
            lambda master: WelcomeScreen(
                master,
                initial_name=self.app_state.user_name,
                on_continue=self._handle_welcome_continue,
            )
        )

    def show_selector(self) -> None:
        self.title("AWS re/Start - Laboratorio")
        self.router.show(
            lambda master: ExerciseSelectorScreen(
                master,
                context=self.context,
                exercises=self.registry.list_by_slots(10),
                on_open_exercise=self.show_exercise,
                on_change_name=self.show_welcome,
            )
        )

    def show_exercise(self, slug: str) -> None:
        self.title("AWS re/Start - Laboratorio")
        exercise = self.registry.get(slug)
        self.app_state.selected_exercise_slug = slug
        self.router.show(
            lambda master: ExerciseHostScreen(
                master,
                context=self.context,
                exercise=exercise,
                on_back=self.show_selector,
            )
        )

    def _handle_welcome_continue(self, user_name: str) -> None:
        self.app_state.user_name = user_name
        self.show_selector()
