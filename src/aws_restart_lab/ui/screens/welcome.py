from collections.abc import Callable
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageTk

from aws_restart_lab.core.assets import get_asset_path
from aws_restart_lab.ui.screens.base import BaseScreen


class WelcomeScreen(BaseScreen):
    BASE_WIDTH = 1536
    BASE_HEIGHT = 1024

    def __init__(
        self,
        master: ctk.CTkFrame,
        initial_name: str,
        on_continue: Callable[[str], None],
    ) -> None:
        super().__init__(master)
        self.on_continue = on_continue
        self._background_source = Image.open(get_asset_path("background.png")).convert("RGB")
        self._background_photo: ImageTk.PhotoImage | None = None
        self._card_photo: ImageTk.PhotoImage | None = None
        self._icon_photo: ImageTk.PhotoImage | None = None
        self._entry_icon_image = ctk.CTkImage(
            light_image=self._make_user_icon(32),
            dark_image=self._make_user_icon(32),
            size=(22, 22),
        )
        self._button_photo: ImageTk.PhotoImage | None = None
        self._button_hover_photo: ImageTk.PhotoImage | None = None
        self._after_resize_id: str | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._schedule_render)

        self.entry_shell = ctk.CTkFrame(
            self.canvas,
            width=480,
            height=66,
            corner_radius=12,
            border_width=1,
            border_color="#b6b7ff",
            fg_color="#ffffff",
        )
        self.entry_shell.grid_columnconfigure(1, weight=1)
        self.entry_shell.grid_rowconfigure(0, weight=1)
        self.entry_shell.grid_propagate(False)

        self.entry_icon = ctk.CTkLabel(
            self.entry_shell,
            text="",
            image=self._entry_icon_image,
            width=44,
            height=44,
            fg_color="transparent",
        )
        self.entry_icon.grid(row=0, column=0, padx=(14, 0), pady=11, sticky="n")

        self.name_entry = ctk.CTkEntry(
            self.entry_shell,
            height=58,
            corner_radius=0,
            border_width=0,
            fg_color="#ffffff",
            text_color="#1b2257",
            placeholder_text="Escribe tu nombre aquí...",
            placeholder_text_color="#8991b3",
            font=ctk.CTkFont(family="Segoe UI", size=20),
        )
        self.name_entry.grid(row=0, column=1, padx=(0, 14), pady=4, sticky="nsew")
        self.name_entry.insert(0, initial_name)
        self.name_entry.bind("<Return>", lambda _event: self._submit())

        self.error_label = ctk.CTkLabel(
            self.canvas,
            text="",
            text_color="#d64545",
            fg_color="transparent",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )

        self.entry_window = self.canvas.create_window(0, 0, window=self.entry_shell, anchor="nw")
        self.error_window = self.canvas.create_window(0, 0, window=self.error_label, anchor="nw")

        self._button_bounds = (0, 0, 0, 0)
        self.canvas.bind("<Button-1>", self._handle_canvas_click)
        self.canvas.bind("<Motion>", self._handle_canvas_motion)
        self._render()

    def on_show(self) -> None:
        pass

    def destroy(self) -> None:
        if self._after_resize_id is not None:
            self.after_cancel(self._after_resize_id)
        super().destroy()

    def _submit(self) -> None:
        name = self.name_entry.get().strip()
        if not name:
            self.error_label.configure(text="Ingresa un nombre para continuar.")
            return

        self.error_label.configure(text="")
        self.on_continue(name)

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

        card_x, card_y = sx(424), sy(191)
        card_w, card_h = ss(688), ss(658)
        self._card_photo = ImageTk.PhotoImage(self._make_card_image(card_w, card_h, ss(28)))
        self.canvas.create_image(card_x, card_y, image=self._card_photo, anchor="nw", tags="drawn")

        icon_size = ss(146)
        icon_x = sx(696)
        icon_y = sy(250)
        self._icon_photo = ImageTk.PhotoImage(self._make_book_icon(icon_size))
        self.canvas.create_image(icon_x, icon_y, image=self._icon_photo, anchor="nw", tags="drawn")

        self.canvas.create_text(
            sx(768),
            sy(452),
            text="¡Bienvenido!",
            fill="#171d51",
            font=("Segoe UI", ss(46), "bold"),
            anchor="center",
            tags="drawn",
        )
        self.canvas.create_text(
            sx(768),
            sy(516),
            text="Nos alegra tenerte aquí.\nPara comenzar, cuéntanos tu nombre.",
            fill="#45527d",
            font=("Segoe UI", ss(22)),
            justify="center",
            anchor="center",
            tags="drawn",
        )
        self.canvas.create_text(
            sx(498),
            sy(592),
            text="¿Cuál es tu nombre?",
            fill="#121849",
            font=("Segoe UI", ss(20), "bold"),
            anchor="nw",
            tags="drawn",
        )

        entry_x, entry_y = sx(498), sy(638)
        entry_w, entry_h = ss(540), ss(67)
        self.entry_shell.configure(
            width=entry_w,
            height=entry_h,
            corner_radius=ss(12),
            border_width=max(1, ss(1)),
        )
        icon_size = max(18, ss(22))
        self._entry_icon_image.configure(size=(icon_size, icon_size))
        self.entry_icon.configure(width=max(34, ss(44)), height=max(34, ss(44)))
        self.name_entry.configure(
            height=max(42, entry_h - ss(8)),
            font=ctk.CTkFont(family="Segoe UI", size=ss(20)),
        )
        self.canvas.coords(self.entry_window, entry_x, entry_y)
        self.canvas.itemconfigure(self.entry_window, width=entry_w, height=entry_h)
        self.canvas.tag_raise(self.entry_window)

        self.error_label.configure(font=ctk.CTkFont(family="Segoe UI", size=ss(13)))
        self.canvas.coords(self.error_window, entry_x, sy(708))
        self.canvas.tag_raise(self.error_window)

        button_x, button_y = sx(498), sy(736)
        button_w, button_h = ss(540), ss(71)
        self._button_bounds = (button_x, button_y, button_x + button_w, button_y + button_h)
        self._button_photo = ImageTk.PhotoImage(
            self._make_gradient_button(button_w, button_h, ss(14), hover=False)
        )
        self._button_hover_photo = ImageTk.PhotoImage(
            self._make_gradient_button(button_w, button_h, ss(14), hover=True)
        )
        self.canvas.create_image(
            button_x,
            button_y,
            image=self._button_photo,
            anchor="nw",
            tags=("drawn", "start_button_image"),
        )
        self.canvas.create_text(
            sx(750),
            sy(772),
            text="Comenzar",
            fill="#ffffff",
            font=("Segoe UI", ss(24), "bold"),
            anchor="center",
            tags=("drawn", "start_button_label"),
        )
        self.canvas.create_text(
            sx(839),
            sy(772),
            text="→",
            fill="#ffffff",
            font=("Segoe UI", ss(31)),
            anchor="center",
            tags=("drawn", "start_button_label"),
        )

    def _draw_background(self, width: int, height: int) -> None:
        image = self._background_source.resize((width, height), Image.Resampling.LANCZOS)
        self._background_photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self._background_photo, anchor="nw", tags="drawn")

    def _make_card_image(self, width: int, height: int, radius: int) -> Image.Image:
        radius = min(radius, width // 2, height // 2)
        shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle((8, 12, width - 8, height - 4), radius, fill=(84, 88, 132, 34))
        shadow = shadow.filter(ImageFilter.GaussianBlur(22))

        card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        card.alpha_composite(shadow)
        draw = ImageDraw.Draw(card)
        draw.rounded_rectangle(
            (0, 0, width - 1, height - 1),
            radius,
            fill=(255, 255, 255, 229),
            outline=(255, 255, 255, 188),
            width=max(1, width // 380),
        )
        return card

    def _make_book_icon(self, size: int) -> Image.Image:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        for y in range(size):
            mix = y / max(size - 1, 1)
            r = round(160 * (1 - mix) + 77 * mix)
            g = round(113 * (1 - mix) + 130 * mix)
            b = round(247 * (1 - mix) + 242 * mix)
            draw.line((0, y, size, y), fill=(r, g, b, 255))

        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((3, 3, size - 3, size - 3), fill=255)
        image.putalpha(mask)

        ring = ImageDraw.Draw(image)
        ring.ellipse((3, 3, size - 3, size - 3), outline=(255, 255, 255, 220), width=max(2, size // 45))

        d = ImageDraw.Draw(image)
        line = (255, 255, 255, 235)
        w = max(2, size // 38)
        d.rounded_rectangle((size * 0.25, size * 0.33, size * 0.50, size * 0.70), radius=size * 0.05, outline=line, width=w)
        d.rounded_rectangle((size * 0.50, size * 0.33, size * 0.75, size * 0.70), radius=size * 0.05, outline=line, width=w)
        d.line((size * 0.50, size * 0.36, size * 0.50, size * 0.72), fill=line, width=w)
        for offset in (0.43, 0.52, 0.61):
            d.line((size * 0.31, size * offset, size * 0.45, size * (offset + 0.02)), fill=line, width=max(1, w - 1))
            d.line((size * 0.55, size * (offset + 0.02), size * 0.69, size * offset), fill=line, width=max(1, w - 1))
        self._draw_sparkle(d, size * 0.20, size * 0.74, size * 0.08, line)
        self._draw_sparkle(d, size * 0.78, size * 0.28, size * 0.08, line)

        return image

    def _make_user_icon(self, size: int) -> Image.Image:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        color = (154, 105, 243, 255)
        draw.ellipse((size * 0.32, size * 0.10, size * 0.68, size * 0.46), fill=color)
        draw.rounded_rectangle(
            (size * 0.16, size * 0.54, size * 0.84, size * 0.92),
            radius=size * 0.16,
            fill=color,
        )
        return image

    def _draw_sparkle(
        self,
        draw: ImageDraw.ImageDraw,
        x: float,
        y: float,
        radius: float,
        color: tuple[int, int, int, int],
    ) -> None:
        width = max(1, round(radius / 5))
        draw.line((x - radius, y, x + radius, y), fill=color, width=width)
        draw.line((x, y - radius, x, y + radius), fill=color, width=width)
        draw.line((x - radius * 0.45, y - radius * 0.45, x + radius * 0.45, y + radius * 0.45), fill=color, width=width)
        draw.line((x - radius * 0.45, y + radius * 0.45, x + radius * 0.45, y - radius * 0.45), fill=color, width=width)

    def _make_gradient_button(self, width: int, height: int, radius: int, hover: bool) -> Image.Image:
        radius = min(radius, width // 2, height // 2)
        left = (172, 83, 238) if not hover else (157, 73, 226)
        right = (84, 143, 247) if not hover else (71, 129, 236)
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(gradient)

        for x in range(width):
            mix = x / max(width - 1, 1)
            color = tuple(round(left[i] * (1 - mix) + right[i] * mix) for i in range(3))
            gdraw.line((x, 0, x, height), fill=(*color, 255))

        mask = Image.new("L", (width, height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
        image.alpha_composite(gradient)
        image.putalpha(mask)
        return image

    def _handle_canvas_click(self, event: tk.Event) -> None:
        x1, y1, x2, y2 = self._button_bounds
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self._submit()

    def _handle_canvas_motion(self, event: tk.Event) -> None:
        x1, y1, x2, y2 = self._button_bounds
        is_hover = x1 <= event.x <= x2 and y1 <= event.y <= y2
        self.canvas.configure(cursor="hand2" if is_hover else "")
        if self._button_hover_photo is not None and self._button_photo is not None:
            self.canvas.itemconfigure(
                "start_button_image",
                image=self._button_hover_photo if is_hover else self._button_photo,
            )
