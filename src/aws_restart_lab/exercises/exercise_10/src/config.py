from __future__ import annotations

from dataclasses import dataclass


WINDOW_TITLE = "Snake Isometrico"
WINDOW_SIZE = "1280x720"
WINDOW_MIN_SIZE = (1024, 640)

CANVAS_WIDTH = 960
CANVAS_HEIGHT = 720
SIDE_PANEL_WIDTH = 320

GRID_COLUMNS = 18
GRID_ROWS = 14
TILE_WIDTH = 56
TILE_HEIGHT = 28
TICK_MS = 180
MARINE_DEAD_TICKS = max(1, round(3000 / TICK_MS))
MARINE_BLINK_TICKS = 10
MARINE_RESPAWN_TICKS = 16
MARINE_MOVE_TICKS = 6
@dataclass(frozen=True)
class LevelConfig:
    number: int
    columns: int
    rows: int
    obstacle_ratio: float
    obstacle_weights: tuple[tuple[str, int], ...]
    marine_count: int
    route_length_range: tuple[int, int]
    biomass_target: int


LEVEL_CONFIGS = (
    LevelConfig(
        number=1,
        columns=18,
        rows=14,
        obstacle_ratio=0.08,
        obstacle_weights=(("rock_1x1", 8), ("crate_1x2_h", 2), ("crate_2x1_v", 2), ("crater_2x2", 0)),
        marine_count=2,
        route_length_range=(2, 2),
        biomass_target=10,
    ),
    LevelConfig(
        number=2,
        columns=20,
        rows=15,
        obstacle_ratio=0.11,
        obstacle_weights=(("rock_1x1", 6), ("crate_1x2_h", 5), ("crate_2x1_v", 5), ("crater_2x2", 1)),
        marine_count=3,
        route_length_range=(2, 3),
        biomass_target=10,
    ),
    LevelConfig(
        number=3,
        columns=22,
        rows=16,
        obstacle_ratio=0.13,
        obstacle_weights=(("rock_1x1", 5), ("crate_1x2_h", 4), ("crate_2x1_v", 4), ("crater_2x2", 2)),
        marine_count=4,
        route_length_range=(3, 4),
        biomass_target=10,
    ),
)
DEFAULT_LEVEL_CONFIG = LEVEL_CONFIGS[0]
LEVEL_NUMBER = DEFAULT_LEVEL_CONFIG.number
BIOMASS_TARGET = DEFAULT_LEVEL_CONFIG.biomass_target
SPRITE_SCALE = 1.0
FLOOR_SPRITE_SIZE = (TILE_WIDTH, TILE_HEIGHT)
WORM_SPRITE_SIZE = (40, 42)
MARINE_SPRITE_SIZE = (54, 68)
MARINE_DEATH_SPRITE_SIZE = (72, 44)
OBSTACLE_SPRITE_SIZES = {
    "rock_1x1": (76, 56),
    "crate_1x2_h": (126, 84),
    "crate_2x1_v": (126, 84),
    "crater_2x2": (124, 84),
}
WORM_ANCHOR_OFFSET = (0, TILE_HEIGHT // 4)
MARINE_ANCHOR_OFFSET = (0, TILE_HEIGHT // 3)
MARINE_DEATH_ANCHOR_OFFSET = (0, TILE_HEIGHT // 4)
OBSTACLE_ANCHOR_OFFSETS = {
    "rock_1x1": (0, TILE_HEIGHT // 2),
    "crate_1x2_h": (0, TILE_HEIGHT // 2),
    "crate_2x1_v": (0, TILE_HEIGHT // 2),
    "crater_2x2": (0, 0),
}
MINIMAP_WIDTH = 184
MINIMAP_HEIGHT = 142
MINIMAP_MARGIN = 18

BACKGROUND_COLOR = "#071426"
CANVAS_COLOR = "#0b1f35"
TILE_COLOR = "#253242"
TILE_ALT_COLOR = "#2a394a"
TILE_OUTLINE_COLOR = "#3f5267"
SNAKE_HEAD_COLOR = "#7ee787"
SNAKE_BODY_COLOR = "#3fb950"
SNAKE_OUTLINE_COLOR = "#d2ffd8"
PANEL_COLOR = "#10243a"
PANEL_BORDER_COLOR = "#263c54"
TEXT_COLOR = "#ffffff"
MUTED_TEXT_COLOR = "#94a3b8"
ACCENT_COLOR = "#ff9900"
