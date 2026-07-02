from collections.abc import Callable, Sequence
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

from aws_restart_lab.core.assets import get_asset_path
from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseDefinition, ExerciseView
from aws_restart_lab.ui.screens.base import BaseScreen


class ExerciseSelectorScreen(BaseScreen):
    BASE_WIDTH = 1536
    BASE_HEIGHT = 1024

    def __init__(
        self,
        master: ctk.CTkFrame,
        context: AppContext,
        exercises: Sequence[ExerciseDefinition | None],
        on_open_exercise: Callable[[str], None],
        on_change_name: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self.context = context
        self.exercises = list(exercises)
        self.on_open_exercise = on_open_exercise
        self.on_change_name = on_change_name

        self._background_source = Image.open(get_asset_path("background.png")).convert("RGB")
        self._background_photo: ImageTk.PhotoImage | None = None
        self._panel_photo: ImageTk.PhotoImage | None = None
        self._after_resize_id: str | None = None
        self._tab_bounds: list[tuple[int, int, int, int, int]] = []
        self._selected_tab_index = self._initial_tab_index()
        self._exercise_view: ExerciseView | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._schedule_render)
        self.canvas.bind("<Button-1>", self._handle_click)
        self.canvas.bind("<Motion>", self._handle_motion)

        self.content_host = ctk.CTkFrame(self.canvas, fg_color="#0a192c", corner_radius=0)
        self.content_host.grid_columnconfigure(0, weight=1)
        self.content_host.grid_rowconfigure(0, weight=1)
        self.content_window = self.canvas.create_window(0, 0, window=self.content_host, anchor="nw")

        self._render()
        self._mount_selected_exercise()

    def on_hide(self) -> None:
        self._unmount_exercise()

    def destroy(self) -> None:
        if self._after_resize_id is not None:
            self.after_cancel(self._after_resize_id)
        self._unmount_exercise()
        super().destroy()

    def _initial_tab_index(self) -> int:
        selected_slug = self.context.state.selected_exercise_slug
        if selected_slug is None:
            return 0

        for index, exercise in enumerate(self.exercises):
            if exercise.slug == selected_slug:
                return index
        return 0

    def _schedule_render(self, _event: tk.Event) -> None:
        if self._after_resize_id is not None:
            self.after_cancel(self._after_resize_id)
        self._after_resize_id = self.after(30, self._render)

    def _render(self) -> None:
        self._after_resize_id = None

        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        if width < 100 or height < 100:
            self._after_resize_id = self.after(30, self._render)
            return

        scale = min(width / self.BASE_WIDTH, height / self.BASE_HEIGHT)
        offset_x = (width - self.BASE_WIDTH * scale) / 2
        offset_y = (height - self.BASE_HEIGHT * scale) / 2

        def sx(value: float) -> int:
            return round(offset_x + value * scale)

        def sy(value: float) -> int:
            return round(offset_y + value * scale)

        def ss(value: float) -> int:
            return max(1, round(value * scale))

        self.canvas.delete("drawn")
        self._draw_background(width, height)
        self._draw_header(sx, sy, ss)
        self._draw_panel_and_tabs(sx, sy, ss)
        self._place_content_host(sx, sy, ss)

    def _draw_background(self, width: int, height: int) -> None:
        image = self._background_source.resize((width, height), Image.Resampling.LANCZOS)
        self._background_photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self._background_photo, anchor="nw", tags="drawn")

    def _draw_header(self, sx: Callable[[float], int], sy: Callable[[float], int], ss: Callable[[float], int]) -> None:
        name = self.context.state.user_name or "Felipe"
        self.canvas.create_text(
            sx(61),
            sy(112),
            text=f"¡Bienvenido, {name}!",
            fill="#ffffff",
            font=("Segoe UI", ss(34), "bold"),
            anchor="nw",
            tags="drawn",
        )
        self.canvas.create_text(
            sx(61),
            sy(168),
            text="Selecciona un ejercicio para comenzar.",
            fill="#ffffff",
            font=("Segoe UI", ss(21)),
            anchor="nw",
            tags="drawn",
        )

        self.canvas.create_text(
            sx(1420),
            sy(119),
            text="aws",
            fill="#ffffff",
            font=("Segoe UI", ss(45), "bold"),
            anchor="center",
            tags="drawn",
        )
        self.canvas.create_arc(
            sx(1378),
            sy(150),
            sx(1465),
            sy(190),
            start=205,
            extent=128,
            style="arc",
            outline="#ff9900",
            width=ss(4),
            tags="drawn",
        )

    def _draw_panel_and_tabs(
        self,
        sx: Callable[[float], int],
        sy: Callable[[float], int],
        ss: Callable[[float], int],
    ) -> None:
        panel_x, panel_y = sx(32), sy(241)
        panel_w, panel_h = ss(1472), ss(746)
        radius = ss(11)
        self._panel_photo = ImageTk.PhotoImage(self._make_panel_image(panel_w, panel_h, radius))
        self.canvas.create_image(panel_x, panel_y, image=self._panel_photo, anchor="nw", tags="drawn")

        tab_h = ss(75)
        tab_count = max(1, len(self.exercises))
        tab_w = panel_w / tab_count
        self._tab_bounds = []

        for index in range(tab_count):
            x1 = round(panel_x + tab_w * index)
            x2 = round(panel_x + tab_w * (index + 1))
            self._tab_bounds.append((x1, panel_y, x2, panel_y + tab_h, index))

            if index > 0:
                self.canvas.create_line(
                    x1,
                    panel_y,
                    x1,
                    panel_y + tab_h,
                    fill="#334155",
                    width=ss(1),
                    tags="drawn",
                )

            label = self._tab_label(index)
            fill = "#ff9900" if index == self._selected_tab_index else "#ffffff"
            self.canvas.create_text(
                round((x1 + x2) / 2),
                sy(280),
                text=label,
                fill=fill,
                font=("Segoe UI", ss(20), "bold" if index == self._selected_tab_index else "normal"),
                anchor="center",
                tags="drawn",
            )

        self.canvas.create_line(
            panel_x,
            panel_y + tab_h,
            panel_x + panel_w,
            panel_y + tab_h,
            fill="#334155",
            width=ss(1),
            tags="drawn",
        )
        active_x1, _, active_x2, _, _ = self._tab_bounds[self._selected_tab_index]
        self.canvas.create_rectangle(
            active_x1,
            panel_y + tab_h - ss(4),
            active_x2,
            panel_y + tab_h,
            fill="#ff9900",
            outline="",
            tags="drawn",
        )

    def _place_content_host(
        self,
        sx: Callable[[float], int],
        sy: Callable[[float], int],
        ss: Callable[[float], int],
    ) -> None:
        content_x, content_y = sx(33), sy(317)
        content_w, content_h = ss(1470), ss(669)
        self.canvas.coords(self.content_window, content_x, content_y)
        self.canvas.itemconfigure(self.content_window, width=content_w, height=content_h)
        self.canvas.tag_raise(self.content_window)

    def _make_panel_image(self, width: int, height: int, radius: int) -> Image.Image:
        radius = min(radius, width // 2, height // 2)
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (0, 0, width - 1, height - 1),
            radius=radius,
            fill=(10, 25, 44, 205),
            outline=(82, 101, 125, 170),
            width=max(1, width // 900),
        )
        return image

    def _tab_label(self, index: int) -> str:
        if index < len(self.exercises):
            return self.exercises[index].title
        return f"Ejercicio {index + 1}"

    def _handle_click(self, event: tk.Event) -> None:
        for x1, y1, x2, y2, index in self._tab_bounds:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self._select_tab(index)
                return

    def _handle_motion(self, event: tk.Event) -> None:
        is_over_tab = any(x1 <= event.x <= x2 and y1 <= event.y <= y2 for x1, y1, x2, y2, _ in self._tab_bounds)
        self.canvas.configure(cursor="hand2" if is_over_tab else "")

    def _select_tab(self, index: int) -> None:
        if index == self._selected_tab_index:
            return
        self._selected_tab_index = index
        self._mount_selected_exercise()
        self._render()

    def _mount_selected_exercise(self) -> None:
        self._unmount_exercise()

        if self._selected_tab_index >= len(self.exercises):
            self.context.state.selected_exercise_slug = None
            return

        exercise = self.exercises[self._selected_tab_index]
        self.context.state.selected_exercise_slug = exercise.slug
        self._exercise_view = exercise.create_view(self.content_host, self.context)
        self._exercise_view.grid(row=0, column=0, sticky="nsew")
        self._exercise_view.on_mount()

    def _unmount_exercise(self) -> None:
        if self._exercise_view is None:
            return

        self._exercise_view.on_unmount()
        self._exercise_view.destroy()
        self._exercise_view = None
