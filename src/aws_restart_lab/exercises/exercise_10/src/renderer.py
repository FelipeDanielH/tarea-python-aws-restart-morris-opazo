from __future__ import annotations

import tkinter as tk
from typing import Any

from .asset_loader import AssetLoader
from .config import (
    CANVAS_COLOR,
    FLOOR_SPRITE_SIZE,
    MARINE_ANCHOR_OFFSET,
    MARINE_DEATH_SPRITE_SIZE,
    MARINE_DEATH_ANCHOR_OFFSET,
    MARINE_SPRITE_SIZE,
    MINIMAP_HEIGHT,
    MINIMAP_MARGIN,
    MINIMAP_WIDTH,
    OBSTACLE_ANCHOR_OFFSETS,
    OBSTACLE_SPRITE_SIZES,
    SNAKE_BODY_COLOR,
    SNAKE_HEAD_COLOR,
    SNAKE_OUTLINE_COLOR,
    TILE_HEIGHT,
    TILE_WIDTH,
    WORM_ANCHOR_OFFSET,
    WORM_SPRITE_SIZE,
)
from .entities import Direction, GridPosition, Marine, Obstacle
from .game_state import GameState
from .level_generator import Level


class IsometricRenderer:
    def __init__(self, canvas: tk.Canvas, asset_loader: AssetLoader) -> None:
        self.canvas = canvas
        self.asset_loader = asset_loader
        self.assets = asset_loader.load_placeholder_assets()
        self._image_refs: list[Any] = []

    def render(self, state: GameState, level: Level) -> None:
        self.canvas.delete("game")
        self._image_refs.clear()
        self.canvas.configure(bg=CANVAS_COLOR)
        origin_x, origin_y = self._calculate_centered_origin(level)
        self._draw_level(level, origin_x, origin_y)
        self._draw_scene(state, level, origin_x, origin_y)
        self._draw_status_text(state)
        self._draw_minimap(state, level)

    def _draw_level(self, level: Level, origin_x: int, origin_y: int) -> None:
        floor = self.asset_loader.image("terrain", "floor.png", size=FLOOR_SPRITE_SIZE, exact_size=True)
        for tile in level.tiles:
            x, y = self._grid_to_screen(tile, origin_x, origin_y)
            if floor is not None:
                self._create_image(x, y, floor, anchor="center")
                self._draw_diamond(x, y, fill="", outline=self.assets["tile_outline"])
                continue

            fill = self.assets["tile_alt"] if (tile.row + tile.col) % 2 else self.assets["tile"]
            self._draw_diamond(
                x,
                y,
                fill=fill,
                outline=self.assets["tile_outline"],
            )

    def _draw_scene(self, state: GameState, level: Level, origin_x: int, origin_y: int) -> None:
        draw_calls: list[tuple[int, int, int, int, int, str, object]] = []
        draw_order = 0
        for obstacle in level.obstacles:
            depth, row, col = self._obstacle_depth(obstacle)
            draw_calls.append((depth, row, col, 0, draw_order, "obstacle", obstacle))
            draw_order += 1

        for index, segment in enumerate(state.snake.segments):
            priority = 2 if index == 0 else 1
            draw_calls.append((segment.row + segment.col, segment.row, segment.col, priority, draw_order, "snake", index))
            draw_order += 1

        for marine in level.marines:
            if marine.is_visible:
                draw_calls.append(
                    (
                        marine.position.row + marine.position.col,
                        marine.position.row,
                        marine.position.col,
                        3,
                        draw_order,
                        "marine",
                        marine,
                    )
                )
                draw_order += 1

        for _depth, _row, _col, _priority, _draw_order, kind, payload in sorted(draw_calls):
            if kind == "obstacle":
                self._draw_obstacle(payload, origin_x, origin_y)  # type: ignore[arg-type]
            elif kind == "snake":
                self._draw_snake_segment(state, int(payload), origin_x, origin_y)
            else:
                self._draw_marine(payload, origin_x, origin_y)  # type: ignore[arg-type]

    def _draw_obstacle(self, obstacle: Obstacle, origin_x: int, origin_y: int) -> None:
        sprite = self.asset_loader.image(
            "terrain",
            self._terrain_filename(obstacle.type),
            size=OBSTACLE_SPRITE_SIZES.get(obstacle.type, (80, 60)),
        )
        if sprite is not None:
            x, y = self._footprint_screen_center(obstacle.occupied_cells, origin_x, origin_y)
            offset_x, offset_y = OBSTACLE_ANCHOR_OFFSETS.get(obstacle.type, (0, TILE_HEIGHT // 2))
            anchor = "center" if "crater" in obstacle.type else "s"
            self._create_image(x + offset_x, y + offset_y, sprite, anchor=anchor)
            return

        self._draw_obstacle_placeholder(obstacle.type, obstacle.occupied_cells, origin_x, origin_y)

    def _draw_marine(self, marine: Marine, origin_x: int, origin_y: int) -> None:
        x, y = self._grid_to_screen(marine.position, origin_x, origin_y)
        sprite_name = self._marine_sprite_name(marine)
        sprite_size = MARINE_DEATH_SPRITE_SIZE if not marine.is_alive else MARINE_SPRITE_SIZE
        sprite = self.asset_loader.image("marine", sprite_name, size=sprite_size)
        if sprite is not None:
            offset_x, offset_y = MARINE_ANCHOR_OFFSET if marine.is_alive else MARINE_DEATH_ANCHOR_OFFSET
            self._create_image(x + offset_x, y + offset_y, sprite, anchor="s")
            return

        if marine.is_alive:
            fill = "#38bdf8"
            outline = "#bae6fd"
        elif marine.state == "dead":
            fill = "#64748b"
            outline = "#cbd5e1"
        else:
            fill = "#f97316"
            outline = "#fed7aa"

        self.canvas.create_oval(
            x - TILE_WIDTH // 5,
            y - TILE_HEIGHT,
            x + TILE_WIDTH // 5,
            y - TILE_HEIGHT // 5,
            fill=fill,
            outline=outline,
            width=2,
            tags="game",
        )
        self.canvas.create_rectangle(
            x - TILE_WIDTH // 7,
            y - TILE_HEIGHT // 3,
            x + TILE_WIDTH // 7,
            y + TILE_HEIGHT // 6,
            fill=fill,
            outline=outline,
            width=1,
            tags="game",
        )

    def _draw_snake_segment(
        self,
        state: GameState,
        index: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        segments = state.snake.segments
        segment = segments[index]
        x, y = self._grid_to_screen(segment, origin_x, origin_y)
        for sprite_name in self._snake_sprite_candidates(state, index):
            sprite = self.asset_loader.image("worm", sprite_name, size=WORM_SPRITE_SIZE)
            if sprite is not None:
                offset_x, offset_y = WORM_ANCHOR_OFFSET
                self._create_image(x + offset_x, y + offset_y, sprite, anchor="s")
                return

        if index == 0:
            self._draw_diamond(
                x,
                y - TILE_HEIGHT // 3,
                fill=SNAKE_HEAD_COLOR,
                outline=SNAKE_OUTLINE_COLOR,
                width=2,
            )
            self.canvas.create_oval(
                x - 4,
                y - TILE_HEIGHT // 2 - 4,
                x + 4,
                y - TILE_HEIGHT // 2 + 4,
                fill="#081526",
                outline="",
                tags="game",
            )
            return

        self._draw_diamond(
            x,
            y - TILE_HEIGHT // 4,
            fill=SNAKE_BODY_COLOR,
            outline=SNAKE_OUTLINE_COLOR,
            width=1,
        )

    def _draw_status_text(self, state: GameState) -> None:
        if state.is_victory:
            status = "Victoria final" if state.level.config.number == 3 else "Nivel completado"
        elif state.is_game_over:
            status = "Game over | pulsa espacio para reintentar"
        elif not state.is_running:
            status = "Pulsa espacio para empezar" if state.message != "Pausado" else "Pausado | pulsa espacio para continuar"
        else:
            status = f"{state.message} | largo {len(state.snake.segments)}"
        self.canvas.create_text(
            24,
            24,
            text=status,
            anchor="nw",
            fill="#94a3b8",
            font=("Segoe UI", 14),
            tags="game",
        )

    def _draw_minimap(self, state: GameState, level: Level) -> None:
        canvas_width = max(self.canvas.winfo_width(), 1)
        x0 = canvas_width - MINIMAP_WIDTH - MINIMAP_MARGIN
        y0 = MINIMAP_MARGIN
        x1 = x0 + MINIMAP_WIDTH
        y1 = y0 + MINIMAP_HEIGHT
        padding = 12

        self.canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            fill="#06111f",
            outline="#2f5f87",
            width=2,
            tags="game",
        )
        self.canvas.create_rectangle(
            x0 + 4,
            y0 + 4,
            x1 - 4,
            y1 - 4,
            outline="#102f4b",
            width=1,
            tags="game",
        )
        self.canvas.create_text(
            x0 + 12,
            y0 + 9,
            text="TACTICAL MAP",
            anchor="nw",
            fill="#7dd3fc",
            font=("Segoe UI", 8, "bold"),
            tags="game",
        )

        map_x0 = x0 + padding
        map_y0 = y0 + 28
        map_width = MINIMAP_WIDTH - padding * 2
        map_height = MINIMAP_HEIGHT - 40
        cell_width = map_width / level.columns
        cell_height = map_height / level.rows

        self.canvas.create_rectangle(
            map_x0,
            map_y0,
            map_x0 + map_width,
            map_y0 + map_height,
            fill="#091827",
            outline="#1d405f",
            width=1,
            tags="game",
        )

        for col in range(1, level.columns):
            x = map_x0 + col * cell_width
            self.canvas.create_line(x, map_y0, x, map_y0 + map_height, fill="#12324b", tags="game")
        for row in range(1, level.rows):
            y = map_y0 + row * cell_height
            self.canvas.create_line(map_x0, y, map_x0 + map_width, y, fill="#12324b", tags="game")

        for obstacle in level.obstacles:
            for cell in obstacle.occupied_cells:
                cx0, cy0, cx1, cy1 = self._minimap_cell_rect(cell, map_x0, map_y0, cell_width, cell_height)
                self.canvas.create_rectangle(
                    cx0,
                    cy0,
                    cx1,
                    cy1,
                    fill="#64748b" if obstacle.blocks_movement else "#334155",
                    outline="",
                    tags="game",
                )

        if len(state.snake.segments) > 1:
            points: list[float] = []
            for segment in state.snake.segments:
                x, y = self._minimap_cell_center(segment, map_x0, map_y0, cell_width, cell_height)
                points.extend((x, y))
            self.canvas.create_line(
                points,
                fill="#7ee787",
                width=2,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
                tags="game",
            )

        head_x, head_y = self._minimap_cell_center(state.snake.segments[0], map_x0, map_y0, cell_width, cell_height)
        self.canvas.create_oval(
            head_x - 3,
            head_y - 3,
            head_x + 3,
            head_y + 3,
            fill="#f8fafc",
            outline="#7ee787",
            width=1,
            tags="game",
        )

        for marine in level.marines:
            x, y = self._minimap_cell_center(marine.position, map_x0, map_y0, cell_width, cell_height)
            fill = "#38bdf8" if marine.is_alive else "#f97316"
            outline = "#bae6fd" if marine.is_alive else "#fed7aa"
            radius = 3 if marine.is_alive else 2
            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill,
                outline=outline,
                width=1,
                tags="game",
            )

        self.canvas.create_rectangle(
            map_x0 - 1,
            map_y0 - 1,
            map_x0 + map_width + 1,
            map_y0 + map_height + 1,
            outline="#38bdf8",
            width=1,
            tags="game",
        )

    def _draw_obstacle_placeholder(
        self,
        obstacle_type: str,
        cells: tuple[GridPosition, ...],
        origin_x: int,
        origin_y: int,
    ) -> None:
        fill, outline = self._obstacle_style(obstacle_type)
        for cell in cells:
            x, y = self._grid_to_screen(cell, origin_x, origin_y)
            if obstacle_type == "crater_2x2":
                self._draw_diamond(x, y + TILE_HEIGHT // 8, fill=fill, outline=outline, width=2)
                self.canvas.create_oval(
                    x - TILE_WIDTH // 5,
                    y - TILE_HEIGHT // 5,
                    x + TILE_WIDTH // 5,
                    y + TILE_HEIGHT // 5,
                    fill="#111827",
                    outline="#4b5563",
                    tags="game",
                )
            else:
                self._draw_diamond(x, y - TILE_HEIGHT // 3, fill=fill, outline=outline, width=2)
                self.canvas.create_rectangle(
                    x - TILE_WIDTH // 5,
                    y - TILE_HEIGHT // 2,
                    x + TILE_WIDTH // 5,
                    y - TILE_HEIGHT // 6,
                    fill=fill,
                    outline=outline,
                    width=1,
                    tags="game",
                )

    def _terrain_filename(self, obstacle_type: str) -> str:
        return {
            "rock_1x1": "rock_1x1.png",
            "crate_1x2_h": "crate_1x2_h.png",
            "crate_2x1_v": "crate_2x1_v.png",
            "crater_2x2": "crater_2x2.png",
        }.get(obstacle_type, f"{obstacle_type}.png")

    def _marine_sprite_name(self, marine: Marine) -> str:
        direction = marine.visual_direction.value
        if not marine.is_alive:
            return f"marine_death_{direction}.png"
        if len(marine.patrol_route) > 1:
            return f"marine_walk_{direction}.png"
        return f"marine_idle_{direction}.png"

    def _snake_sprite_candidates(self, state: GameState, index: int) -> tuple[str, ...]:
        if index == 0:
            return (self._worm_head_asset_name(state.snake.direction),)

        body_direction = self._snake_body_direction(state.snake.segments, index)
        body = f"worm_body_{self._worm_body_asset_direction(body_direction).value}.png"
        turn = self._snake_turn_name(state.snake.segments, index)
        if turn is None:
            return (body,)
        return (turn, body)

    def _snake_turn_name(self, segments: list[GridPosition], index: int) -> str | None:
        if index <= 0 or index >= len(segments) - 1:
            return None

        current = segments[index]
        toward_head = self._direction_between(current, segments[index - 1])
        toward_tail = self._direction_between(current, segments[index + 1])
        if (
            toward_head is None
            or toward_tail is None
            or toward_head == toward_tail
            or toward_head.is_opposite(toward_tail)
        ):
            return None

        turn_assets = {
            frozenset((Direction.NE, Direction.NW)): "worm_turn_NE_NW.png",
            frozenset((Direction.NW, Direction.SW)): "worm_turn_NW_SW.png",
            frozenset((Direction.SW, Direction.SE)): "worm_turn_SW_SE.png",
            frozenset((Direction.SE, Direction.NE)): "worm_turn_SE_NE.png",
        }
        return turn_assets.get(frozenset((toward_head, toward_tail)))

    def _snake_body_direction(self, segments: list[GridPosition], index: int) -> Direction:
        if index > 0:
            toward_head = self._direction_between(segments[index], segments[index - 1])
            if toward_head is not None:
                return toward_head
        if index < len(segments) - 1:
            away_from_tail = self._direction_between(segments[index + 1], segments[index])
            if away_from_tail is not None:
                return away_from_tail
        return Direction.SE

    def _direction_between(self, start: GridPosition, end: GridPosition) -> Direction | None:
        delta = (end.row - start.row, end.col - start.col)
        for direction in Direction:
            if direction.delta == delta:
                return direction
        return None

    def _worm_head_asset_name(self, direction: Direction) -> str:
        if direction == Direction.NW:
            return "worm_turn_NW_SW.png"

        asset_direction = {
            Direction.NE: Direction.NE,
            Direction.SW: Direction.NE,
            Direction.SE: Direction.NW,
        }[direction]
        return f"worm_head_{asset_direction.value}.png"

    def _worm_body_asset_direction(self, direction: Direction) -> Direction:
        return {
            Direction.NE: Direction.NW,
            Direction.NW: Direction.NE,
            Direction.SE: Direction.SE,
            Direction.SW: Direction.SW,
        }[direction]

    def _obstacle_style(self, obstacle_type: str) -> tuple[str, str]:
        return {
            "rock_1x1": ("#64748b", "#cbd5e1"),
            "crate_1x2_h": ("#a16207", "#facc15"),
            "crate_2x1_v": ("#92400e", "#fdba74"),
            "crater_2x2": ("#312e2b", "#78716c"),
        }.get(obstacle_type, ("#7c3aed", "#ddd6fe"))

    def _obstacle_depth(self, obstacle: Obstacle) -> tuple[int, int, int]:
        deepest_cell = max(
            obstacle.occupied_cells,
            key=lambda cell: (cell.row + cell.col, cell.row, cell.col),
        )
        return deepest_cell.row + deepest_cell.col, deepest_cell.row, deepest_cell.col

    def _calculate_centered_origin(self, level: Level) -> tuple[int, int]:
        canvas_width = max(self.canvas.winfo_width(), 1)
        canvas_height = max(self.canvas.winfo_height(), 1)

        raw_points = [self._grid_to_screen(tile, 0, 0) for tile in level.tiles]
        min_x = min(x - TILE_WIDTH // 2 for x, _ in raw_points)
        max_x = max(x + TILE_WIDTH // 2 for x, _ in raw_points)
        min_y = min(y - TILE_HEIGHT // 2 for _, y in raw_points)
        max_y = max(y + TILE_HEIGHT // 2 for _, y in raw_points)

        map_width = max_x - min_x
        map_height = max_y - min_y
        origin_x = int((canvas_width - map_width) / 2 - min_x)
        origin_y = int((canvas_height - map_height) / 2 - min_y)
        return origin_x, origin_y

    def _grid_to_screen(self, position: GridPosition, origin_x: int, origin_y: int) -> tuple[int, int]:
        x = origin_x + (position.col - position.row) * (TILE_WIDTH // 2)
        y = origin_y + (position.col + position.row) * (TILE_HEIGHT // 2)
        return x, y

    def _footprint_screen_center(
        self,
        cells: tuple[GridPosition, ...],
        origin_x: int,
        origin_y: int,
    ) -> tuple[int, int]:
        points = [self._grid_to_screen(cell, origin_x, origin_y) for cell in cells]
        x = round(sum(point[0] for point in points) / len(points))
        y = round(sum(point[1] for point in points) / len(points))
        return x, y

    def _minimap_cell_center(
        self,
        position: GridPosition,
        map_x0: float,
        map_y0: float,
        cell_width: float,
        cell_height: float,
    ) -> tuple[float, float]:
        return (
            map_x0 + (position.col + 0.5) * cell_width,
            map_y0 + (position.row + 0.5) * cell_height,
        )

    def _minimap_cell_rect(
        self,
        position: GridPosition,
        map_x0: float,
        map_y0: float,
        cell_width: float,
        cell_height: float,
    ) -> tuple[float, float, float, float]:
        inset = 0.5
        return (
            map_x0 + position.col * cell_width + inset,
            map_y0 + position.row * cell_height + inset,
            map_x0 + (position.col + 1) * cell_width - inset,
            map_y0 + (position.row + 1) * cell_height - inset,
        )

    def _create_image(self, x: int, y: int, image: Any, anchor: str) -> None:
        self._image_refs.append(image)
        self.canvas.create_image(x, y, image=image, anchor=anchor, tags="game")

    def _draw_diamond(self, x: int, y: int, fill: str, outline: str, width: int = 1) -> None:
        half_w = TILE_WIDTH // 2
        half_h = TILE_HEIGHT // 2
        points = (
            x,
            y - half_h,
            x + half_w,
            y,
            x,
            y + half_h,
            x - half_w,
            y,
        )
        self.canvas.create_polygon(points, fill=fill, outline=outline, width=width, tags="game")
