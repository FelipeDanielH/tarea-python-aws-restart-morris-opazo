from __future__ import annotations

import random
import tkinter as tk

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView

from .asset_loader import AssetLoader
from .config import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    CANVAS_COLOR,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    LEVEL_CONFIGS,
    MUTED_TEXT_COLOR,
    PANEL_BORDER_COLOR,
    PANEL_COLOR,
    SIDE_PANEL_WIDTH,
    TEXT_COLOR,
    TICK_MS,
    WINDOW_MIN_SIZE,
    WINDOW_SIZE,
    WINDOW_TITLE,
)
from .entities import Direction
from .game_state import GameState
from .input_handler import InputHandler
from .level_generator import LevelGenerator
from .renderer import IsometricRenderer


class SnakeGameApp(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext | None = None) -> None:
        super().__init__(master, context)  # type: ignore[arg-type]

        self.configure(fg_color=BACKGROUND_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.level_generator = LevelGenerator()
        self.current_seed = self._generate_seed()
        self.current_level_index = 0
        self.level = self._create_level()
        self.state = GameState.initial(self.level)
        self.asset_loader = AssetLoader()
        self._tick_after_id: str | None = None

        self.canvas = tk.Canvas(
            self,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=CANVAS_COLOR,
            highlightthickness=0,
            bd=0,
            takefocus=1,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.side_panel = ctk.CTkFrame(
            self,
            width=SIDE_PANEL_WIDTH,
            fg_color=PANEL_COLOR,
            border_width=1,
            border_color=PANEL_BORDER_COLOR,
            corner_radius=0,
        )
        self.side_panel.grid(row=0, column=1, sticky="nsew")
        self.side_panel.grid_propagate(False)
        self.side_panel.grid_columnconfigure(0, weight=1)

        self._build_side_panel()

        self.renderer = IsometricRenderer(self.canvas, self.asset_loader)
        self.input_handler = InputHandler(self.canvas, self._set_direction, self._toggle_running)
        self.canvas.bind("<Configure>", lambda _event: self.render())

    def on_mount(self) -> None:
        self.canvas.focus_set()
        self.input_handler.bind()
        self.render()

    def on_unmount(self) -> None:
        self._cancel_tick()
        self.input_handler.unbind()

    def render(self) -> None:
        self.renderer.render(self.state, self.level)
        self._sync_panel()

    def _build_side_panel(self) -> None:
        self.side_panel.grid_rowconfigure(9, weight=1)

        title = ctk.CTkLabel(
            self.side_panel,
            text="Worm Protocol",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, padx=24, pady=(28, 8), sticky="ew")

        subtitle = ctk.CTkLabel(
            self.side_panel,
            text="Laboratorio isométrico de biomasa.",
            text_color=MUTED_TEXT_COLOR,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 18), sticky="ew")

        self.status_badge = ctk.CTkLabel(
            self.side_panel,
            text="LISTO",
            text_color="#081526",
            fg_color=ACCENT_COLOR,
            corner_radius=6,
            height=34,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.status_badge.grid(row=2, column=0, padx=24, pady=(0, 22), sticky="ew")

        self.biomass_label = self._create_stat_label(3, "Marines", f"0 / {self.level.config.biomass_target}")
        self.level_label = self._create_stat_label(4, "Nivel", str(self.level.config.number))
        self.length_label = self._create_stat_label(5, "Longitud", "3")

        self.start_button = ctk.CTkButton(
            self.side_panel,
            text="Iniciar / Espacio",
            fg_color=ACCENT_COLOR,
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._toggle_running,
        )
        self.start_button.grid(row=10, column=0, padx=24, pady=(0, 12), sticky="ew")

        self.restart_button = ctk.CTkButton(
            self.side_panel,
            text="Reiniciar Nivel",
            fg_color="#1f3b57",
            hover_color="#284a6b",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._reset_game,
        )
        self.restart_button.grid(row=11, column=0, padx=24, pady=(0, 12), sticky="ew")

        controls_hint = ctk.CTkLabel(
            self.side_panel,
            text="Flechas o WASD: NE / NW / SE / SW",
            text_color=MUTED_TEXT_COLOR,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            anchor="nw",
            justify="left",
            wraplength=250,
        )
        controls_hint.grid(row=12, column=0, padx=24, pady=(0, 24), sticky="ew")

    def _create_stat_label(self, row: int, label: str, value: str) -> ctk.CTkLabel:
        stat = ctk.CTkLabel(
            self.side_panel,
            text=f"{label}\n{value}",
            text_color=TEXT_COLOR,
            fg_color="#0c1d31",
            corner_radius=8,
            height=54,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            anchor="w",
            justify="left",
            padx=14,
        )
        stat.grid(row=row, column=0, padx=24, pady=(0, 10), sticky="ew")
        return stat

    def _set_direction(self, direction: Direction) -> None:
        self.state.change_direction(direction)
        self.render()

    def _toggle_running(self) -> None:
        self.canvas.focus_set()
        if self.state.is_running:
            self.state.pause()
            self._cancel_tick()
            self.render()
            return

        self.state.start()
        self.render()
        self._schedule_tick()

    def _reset_game(self) -> None:
        self._cancel_tick()
        self.level = self._create_level()
        self.state = GameState.initial(self.level)
        self.render()
        self.canvas.focus_set()

    def _new_seed(self) -> None:
        self._cancel_tick()
        self.current_seed = self._generate_seed()
        self.current_level_index = 0
        self.level = self._create_level()
        self.state = GameState.initial(self.level)
        self.render()
        self.canvas.focus_set()

    def _create_level(self):
        level_config = LEVEL_CONFIGS[self.current_level_index]
        level_seed = f"{self.current_seed}:level:{level_config.number}"
        return self.level_generator.create_default_level(seed=level_seed, config=level_config)

    def _generate_seed(self) -> int:
        return random.SystemRandom().randint(100000, 999999)

    def _schedule_tick(self) -> None:
        self._cancel_tick()
        if not self.state.is_victory and (self.state.is_running or self.state.has_pending_marine_respawns()):
            self._tick_after_id = self.after(TICK_MS, self._tick)

    def _tick(self) -> None:
        self._tick_after_id = None
        if self.state.is_running and not self.state.is_game_over:
            self.state.tick()
            if self.state.is_victory and self._has_next_level():
                self._advance_level()
        else:
            if not self.state.is_victory:
                self.state.update_world_timers()
        self.render()
        if not self.state.is_victory and (self.state.is_running or self.state.has_pending_marine_respawns()):
            self._schedule_tick()

    def _has_next_level(self) -> bool:
        return self.current_level_index < len(LEVEL_CONFIGS) - 1

    def _advance_level(self) -> None:
        self.current_level_index += 1
        self.level = self._create_level()
        self.state = GameState.initial(self.level)
        self.state.message = "Pulsa espacio para empezar."
        self.state.is_running = False

    def _cancel_tick(self) -> None:
        if self._tick_after_id is not None:
            self.after_cancel(self._tick_after_id)
            self._tick_after_id = None

    def _sync_panel(self) -> None:
        status_text, status_color, status_text_color = self._hud_status()

        self.status_badge.configure(text=status_text, fg_color=status_color, text_color=status_text_color)
        self.biomass_label.configure(text=f"Marines\n{self.state.score} / {self.level.config.biomass_target}")
        self.level_label.configure(text=f"Nivel\n{self.level.config.number} / {len(LEVEL_CONFIGS)}")
        self.length_label.configure(text=f"Longitud\n{len(self.state.snake.segments)}")
        if self.state.is_game_over:
            self.start_button.configure(text="Jugar otra vez")
        elif self.state.is_victory:
            self.start_button.configure(text="Victoria final")
        elif self.state.is_running:
            self.start_button.configure(text="Pausar")
        else:
            self.start_button.configure(text="Iniciar / Espacio")

    def _hud_status(self) -> tuple[str, str, str]:
        if self.state.is_victory:
            return "VICTORIA FINAL", "#7ee787", "#071426"
        if self.state.is_game_over:
            return "GAME OVER", "#ef4444", "#ffffff"
        if self.state.is_running:
            return "JUGANDO", ACCENT_COLOR, "#081526"
        if self.state.message == "Pausado":
            return "PAUSADO", "#38bdf8", "#071426"
        return "LISTO", "#64748b", "#ffffff"


class SnakeGameWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*WINDOW_MIN_SIZE)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.game = SnakeGameApp(self, context=None)
        self.game.grid(row=0, column=0, sticky="nsew")
        self.after(0, self.game.on_mount)

    def destroy(self) -> None:
        self.game.on_unmount()
        super().destroy()
