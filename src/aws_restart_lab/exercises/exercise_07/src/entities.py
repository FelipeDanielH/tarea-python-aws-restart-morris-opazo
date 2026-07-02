from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class GridPosition:
    row: int
    col: int


class Direction(Enum):
    NE = "NE"
    NW = "NW"
    SE = "SE"
    SW = "SW"

    @property
    def delta(self) -> tuple[int, int]:
        return {
            Direction.NE: (-1, 0),
            Direction.NW: (0, -1),
            Direction.SE: (0, 1),
            Direction.SW: (1, 0),
        }[self]

    def is_opposite(self, other: "Direction") -> bool:
        return {
            Direction.NE: Direction.SW,
            Direction.SW: Direction.NE,
            Direction.NW: Direction.SE,
            Direction.SE: Direction.NW,
        }[self] == other


@dataclass
class Snake:
    segments: list[GridPosition]
    direction: Direction = Direction.SE


@dataclass
class Marine:
    position: GridPosition
    state: str = "idle"
    visual_direction: Direction = Direction.SW
    is_alive: bool = True
    patrol_route: tuple[GridPosition, ...] = ()
    route_index: int = 0
    route_step: int = 1
    patrol_phase: int = 0
    move_ticks: int = 0
    dead_ticks: int = 0
    blink_ticks: int = 0
    respawn_ticks: int = 0

    @property
    def is_visible(self) -> bool:
        if self.is_alive:
            return True
        if self.state == "dead":
            return True
        if self.state == "dying":
            return self.blink_ticks % 2 == 0
        return False


@dataclass(frozen=True)
class Obstacle:
    type: str
    base_position: GridPosition
    footprint: tuple[GridPosition, ...]
    blocks_movement: bool = True

    @property
    def occupied_cells(self) -> tuple[GridPosition, ...]:
        return tuple(
            GridPosition(
                row=self.base_position.row + offset.row,
                col=self.base_position.col + offset.col,
            )
            for offset in self.footprint
        )
