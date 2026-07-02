from __future__ import annotations

from dataclasses import dataclass
from random import Random
from collections import deque

from .config import DEFAULT_LEVEL_CONFIG, LevelConfig, MARINE_MOVE_TICKS
from .entities import Direction, GridPosition, Marine, Obstacle


@dataclass(frozen=True)
class Level:
    columns: int
    rows: int
    tiles: tuple[GridPosition, ...]
    obstacles: tuple[Obstacle, ...]
    marines: tuple[Marine, ...]
    safe_zone: frozenset[GridPosition]
    config: LevelConfig

    def is_inside_bounds(self, position: GridPosition) -> bool:
        return 0 <= position.row < self.rows and 0 <= position.col < self.columns

    def blocked_cells(self) -> set[GridPosition]:
        cells: set[GridPosition] = set()
        for obstacle in self.obstacles:
            if obstacle.blocks_movement:
                cells.update(obstacle.occupied_cells)
        return cells

    def is_blocked(self, position: GridPosition) -> bool:
        return position in self.blocked_cells()

    def free_cells(self) -> set[GridPosition]:
        return set(self.tiles) - self.blocked_cells()

    def reachable_cells(
        self,
        start: GridPosition,
        extra_blocked: set[GridPosition] | None = None,
    ) -> set[GridPosition]:
        blocked = self.blocked_cells() | (extra_blocked or set())
        if start in blocked or not self.is_inside_bounds(start):
            return set()

        visited = {start}
        queue: deque[GridPosition] = deque([start])
        deltas = ((-1, 0), (0, -1), (0, 1), (1, 0))

        while queue:
            current = queue.popleft()
            for delta_row, delta_col in deltas:
                neighbor = GridPosition(row=current.row + delta_row, col=current.col + delta_col)
                if (
                    neighbor not in visited
                    and neighbor not in blocked
                    and self.is_inside_bounds(neighbor)
                ):
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited

    def reachable_ratio_from(self, start: GridPosition) -> float:
        free = self.free_cells()
        if not free:
            return 0.0
        return len(self.reachable_cells(start)) / len(free)


class LevelGenerationError(RuntimeError):
    """Raised when procedural generation cannot produce a valid map."""


class LevelGenerator:
    OBSTACLE_FOOTPRINTS: dict[str, tuple[tuple[int, int], ...]] = {
        "rock_1x1": ((0, 0),),
        "crate_1x2_h": ((0, 0), (0, 1)),
        "crate_2x1_v": ((0, 0), (1, 0)),
        "crater_2x2": ((0, 0), (0, 1), (1, 0), (1, 1)),
    }
    MAX_PLACEMENT_ATTEMPTS = 180
    MAX_MAP_ATTEMPTS = 40
    SAFE_RADIUS = 3
    MIN_REACHABLE_RATIO = 0.75
    MARINE_ROUTE_ATTEMPTS = 160

    def create_default_level(
        self,
        seed: int | str | None = None,
        config: LevelConfig = DEFAULT_LEVEL_CONFIG,
        snake_spawn: tuple[GridPosition, ...] | None = None,
    ) -> Level:
        rng = Random(seed)
        tiles = tuple(
            GridPosition(row=row, col=col)
            for row in range(config.rows)
            for col in range(config.columns)
        )
        spawn = snake_spawn or self.default_snake_spawn(config)
        safe_zone = self._build_safe_zone(spawn, config)

        for _ in range(self.MAX_MAP_ATTEMPTS):
            obstacles = self._generate_obstacles(rng, config, safe_zone, set(spawn))
            level = Level(
                columns=config.columns,
                rows=config.rows,
                tiles=tiles,
                obstacles=obstacles,
                marines=(),
                safe_zone=frozenset(safe_zone),
                config=config,
            )
            if self._is_valid_level(level, spawn, safe_zone):
                marines = self._generate_marines(rng, config, level, spawn, safe_zone)
                level = Level(
                    columns=config.columns,
                    rows=config.rows,
                    tiles=tiles,
                    obstacles=obstacles,
                    marines=marines,
                    safe_zone=frozenset(safe_zone),
                    config=config,
                )
                return level

        raise LevelGenerationError(
            "No se pudo generar un mapa jugable con las restricciones actuales."
        )

    def default_snake_spawn(self, config: LevelConfig = DEFAULT_LEVEL_CONFIG) -> tuple[GridPosition, ...]:
        row = max(2, config.rows // 2 - 1)
        col = max(3, config.columns // 3)
        return (
            GridPosition(row=row, col=col),
            GridPosition(row=row, col=col - 1),
            GridPosition(row=row, col=col - 2),
        )

    def _generate_obstacles(
        self,
        rng: Random,
        config: LevelConfig,
        safe_zone: set[GridPosition],
        spawn_cells: set[GridPosition],
    ) -> tuple[Obstacle, ...]:
        obstacles: list[Obstacle] = []
        occupied: set[GridPosition] = set()
        target_blocked_cells = int(config.columns * config.rows * config.obstacle_ratio)

        for _ in range(self.MAX_PLACEMENT_ATTEMPTS):
            if len(occupied) >= target_blocked_cells:
                break

            obstacle_type = self._weighted_obstacle_type(rng, config)
            row = rng.randrange(config.rows)
            col = rng.randrange(config.columns)
            obstacle = self._obstacle(
                obstacle_type,
                row,
                col,
                self.OBSTACLE_FOOTPRINTS[obstacle_type],
                True,
            )

            if not self._can_place(obstacle, config, occupied, safe_zone, spawn_cells):
                continue

            obstacles.append(obstacle)
            occupied.update(obstacle.occupied_cells)

        return tuple(obstacles)

    def _weighted_obstacle_type(self, rng: Random, config: LevelConfig) -> str:
        weighted = tuple((obstacle_type, weight) for obstacle_type, weight in config.obstacle_weights if weight > 0)
        population = [obstacle_type for obstacle_type, _weight in weighted]
        weights = [weight for _obstacle_type, weight in weighted]
        return rng.choices(population, weights=weights, k=1)[0]

    def _can_place(
        self,
        obstacle: Obstacle,
        config: LevelConfig,
        occupied: set[GridPosition],
        safe_zone: set[GridPosition],
        spawn_cells: set[GridPosition],
    ) -> bool:
        cells = set(obstacle.occupied_cells)
        return (
            all(self._is_inside_bounds(cell, config) for cell in cells)
            and cells.isdisjoint(safe_zone)
            and cells.isdisjoint(spawn_cells)
            and cells.isdisjoint(occupied)
        )

    def _build_safe_zone(self, spawn_cells: tuple[GridPosition, ...], config: LevelConfig) -> set[GridPosition]:
        safe_zone: set[GridPosition] = set()
        for spawn in spawn_cells:
            for row in range(spawn.row - self.SAFE_RADIUS, spawn.row + self.SAFE_RADIUS + 1):
                for col in range(spawn.col - self.SAFE_RADIUS, spawn.col + self.SAFE_RADIUS + 1):
                    candidate = GridPosition(row=row, col=col)
                    if self._is_inside_bounds(candidate, config):
                        safe_zone.add(candidate)
        return safe_zone

    def _is_valid_level(
        self,
        level: Level,
        spawn_cells: tuple[GridPosition, ...],
        safe_zone: set[GridPosition],
    ) -> bool:
        blocked = level.blocked_cells()
        if any(cell in blocked for cell in spawn_cells):
            return False
        if any(cell in blocked for cell in safe_zone):
            return False

        reachable = level.reachable_cells(spawn_cells[0])
        free = level.free_cells()
        if not free:
            return False

        reachable_ratio = len(reachable) / len(free)
        if reachable_ratio < self.MIN_REACHABLE_RATIO:
            return False

        # Avoid large disconnected islands that become unreachable dead zones.
        disconnected = free - reachable
        return len(disconnected) <= int(len(free) * (1 - self.MIN_REACHABLE_RATIO))

    def _generate_marines(
        self,
        rng: Random,
        config: LevelConfig,
        level: Level,
        spawn_cells: tuple[GridPosition, ...],
        safe_zone: set[GridPosition],
    ) -> tuple[Marine, ...]:
        reachable = level.reachable_cells(spawn_cells[0])
        forbidden = set(spawn_cells) | safe_zone | level.blocked_cells()
        candidates = sorted(reachable - forbidden, key=lambda position: (position.row, position.col))
        rng.shuffle(candidates)

        target_count = config.marine_count
        marines: list[Marine] = []
        used_route_cells: set[GridPosition] = set()

        for candidate in candidates:
            if len(marines) >= target_count:
                break
            route = self._create_marine_route(rng, config, candidate, candidates, used_route_cells)
            if route is None:
                continue
            route_cells = set(route)
            patrol_phase = (MARINE_MOVE_TICKS - 1 - len(marines)) % MARINE_MOVE_TICKS
            marines.append(
                Marine(
                    position=route[0],
                    state="idle",
                    visual_direction=self._route_direction(route),
                    is_alive=True,
                    patrol_route=route,
                    route_index=0,
                    route_step=1,
                    patrol_phase=patrol_phase,
                    move_ticks=patrol_phase,
                )
            )
            used_route_cells.update(route_cells)

        return tuple(marines)

    def _create_marine_route(
        self,
        rng: Random,
        config: LevelConfig,
        start: GridPosition,
        valid_cells: list[GridPosition],
        used_route_cells: set[GridPosition],
    ) -> tuple[GridPosition, ...] | None:
        valid = set(valid_cells)
        if start in used_route_cells:
            return None

        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        lengths = list(range(config.route_length_range[0], config.route_length_range[1] + 1))

        for _ in range(self.MARINE_ROUTE_ATTEMPTS):
            delta_row, delta_col = rng.choice(directions)
            length = rng.choice(lengths)
            route = tuple(
                GridPosition(row=start.row + delta_row * offset, col=start.col + delta_col * offset)
                for offset in range(length)
            )
            route_cells = set(route)
            if route_cells.issubset(valid) and route_cells.isdisjoint(used_route_cells):
                return route

        return None

    def _route_direction(self, route: tuple[GridPosition, ...]) -> Direction:
        if len(route) < 2:
            return Direction.SW

        delta = (route[1].row - route[0].row, route[1].col - route[0].col)
        for direction in Direction:
            if direction.delta == delta:
                return direction
        return Direction.SW

    def _is_inside_bounds(self, position: GridPosition, config: LevelConfig) -> bool:
        return 0 <= position.row < config.rows and 0 <= position.col < config.columns

    def _obstacle(
        self,
        obstacle_type: str,
        row: int,
        col: int,
        footprint: tuple[tuple[int, int], ...],
        blocks_movement: bool,
    ) -> Obstacle:
        return Obstacle(
            type=obstacle_type,
            base_position=GridPosition(row=row, col=col),
            footprint=tuple(GridPosition(row=offset_row, col=offset_col) for offset_row, offset_col in footprint),
            blocks_movement=blocks_movement,
        )
