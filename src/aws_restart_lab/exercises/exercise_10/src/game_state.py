from __future__ import annotations

from dataclasses import dataclass

from .config import MARINE_BLINK_TICKS, MARINE_DEAD_TICKS, MARINE_MOVE_TICKS, MARINE_RESPAWN_TICKS
from .entities import Direction, GridPosition, Marine, Snake
from .level_generator import Level


@dataclass
class GameState:
    level: Level
    snake: Snake
    score: int = 0
    is_running: bool = False
    is_game_over: bool = False
    is_victory: bool = False
    message: str = "Pulsa espacio para empezar."

    @classmethod
    def initial(cls, level: Level) -> "GameState":
        snake = Snake(
            segments=list(cls._default_snake_spawn(level)),
            direction=Direction.SE,
        )
        return cls(level=level, snake=snake)

    @staticmethod
    def _default_snake_spawn(level: Level) -> tuple[GridPosition, ...]:
        row = max(2, level.rows // 2 - 1)
        col = max(3, level.columns // 3)
        return (
            GridPosition(row=row, col=col),
            GridPosition(row=row, col=col - 1),
            GridPosition(row=row, col=col - 2),
        )

    def start(self) -> None:
        if self.is_game_over or self.is_victory:
            self.reset()
        self.is_running = True
        self.message = "Jugando"

    def pause(self) -> None:
        if self.is_game_over or self.is_victory:
            return
        self.is_running = False
        self.message = "Pausado"

    def reset(self) -> None:
        fresh = self.initial(self.level)
        self.level = fresh.level
        self.snake = fresh.snake
        self.score = fresh.score
        self.is_running = fresh.is_running
        self.is_game_over = fresh.is_game_over
        self.is_victory = fresh.is_victory
        self.message = fresh.message

    def change_direction(self, direction: Direction) -> None:
        if len(self.snake.segments) > 1 and direction.is_opposite(self.snake.direction):
            return
        self.snake.direction = direction

    def tick(self) -> None:
        if not self.is_running or self.is_game_over or self.is_victory:
            return

        self.update_world_timers()

        next_head = self._next_head()
        target_marine = self._marine_at(next_head)
        will_consume_marine = target_marine is not None
        body_to_check = self.snake.segments if will_consume_marine else self.snake.segments[:-1]

        if not self._is_inside_bounds(next_head) or self.is_cell_blocked(next_head) or next_head in body_to_check:
            self.is_running = False
            self.is_game_over = True
            self.message = "Game over"
            return

        self.snake.segments.insert(0, next_head)
        if target_marine is not None:
            self.score += 1
            self._consume_marine(target_marine)
            if self._is_level_objective_complete():
                self.is_running = False
                self.is_victory = True
                self.message = "Nivel completado"
            else:
                self.message = "Marine consumido"
        else:
            self.snake.segments.pop()
            self.message = "Jugando"

    def update_world_timers(self) -> None:
        self._update_marine_lifecycle()
        if not self.is_game_over:
            self._update_marine_patrols()

    def has_pending_marine_respawns(self) -> bool:
        return any(not marine.is_alive for marine in self.level.marines)

    def _is_level_objective_complete(self) -> bool:
        return self.score >= self.level.config.biomass_target

    def _next_head(self) -> GridPosition:
        head = self.snake.segments[0]
        delta_row, delta_col = self.snake.direction.delta
        return GridPosition(row=head.row + delta_row, col=head.col + delta_col)

    def _is_inside_bounds(self, position: GridPosition) -> bool:
        return self.level.is_inside_bounds(position)

    def is_cell_blocked(self, position: GridPosition) -> bool:
        return self.level.is_blocked(position)

    def _marine_at(self, position: GridPosition) -> Marine | None:
        for marine in self.level.marines:
            if marine.is_alive and marine.position == position:
                return marine
        return None

    def _consume_marine(self, marine: Marine) -> None:
        marine.is_alive = False
        marine.state = "dead"
        marine.dead_ticks = 0
        marine.blink_ticks = 0
        marine.respawn_ticks = 0

    def _update_marine_lifecycle(self) -> None:
        for marine in self.level.marines:
            if marine.is_alive:
                continue

            if marine.state == "dead":
                marine.dead_ticks += 1
                if marine.dead_ticks >= MARINE_DEAD_TICKS:
                    marine.state = "dying"
                    marine.blink_ticks = 0
                continue

            if marine.state == "dying":
                marine.blink_ticks += 1
                if marine.blink_ticks >= MARINE_BLINK_TICKS:
                    marine.state = "respawning"
                    marine.respawn_ticks = 0
                continue

            if marine.state == "respawning":
                marine.respawn_ticks += 1
                if marine.respawn_ticks >= MARINE_RESPAWN_TICKS:
                    self._respawn_marine(marine)

    def _respawn_marine(self, marine: Marine) -> None:
        next_position = self._next_marine_spawn_position(exclude=marine)
        if next_position is None:
            marine.respawn_ticks = max(0, MARINE_RESPAWN_TICKS - 4)
            return

        marine.position = next_position
        marine.state = "idle"
        marine.is_alive = True
        marine.route_index = 0
        marine.route_step = 1
        marine.move_ticks = self._patrol_phase_for(marine)
        if len(marine.patrol_route) > 1:
            next_direction = self._direction_between(marine.patrol_route[0], marine.patrol_route[1])
            if next_direction is not None:
                marine.visual_direction = next_direction
        marine.dead_ticks = 0
        marine.blink_ticks = 0
        marine.respawn_ticks = 0

    def _patrol_phase_for(self, marine: Marine) -> int:
        if MARINE_MOVE_TICKS <= 1:
            return 0
        route_weight = sum(cell.row + cell.col for cell in marine.patrol_route)
        return (marine.patrol_phase + route_weight + len(marine.patrol_route)) % MARINE_MOVE_TICKS

    def _next_marine_spawn_position(self, exclude: Marine) -> GridPosition | None:
        route = self._next_marine_patrol_route(exclude=exclude)
        if route is None:
            return None

        exclude.patrol_route = route
        return route[0]

    def _next_marine_patrol_route(self, exclude: Marine) -> tuple[GridPosition, ...] | None:
        snake_cells = set(self.snake.segments)
        occupied_marines = {
            marine.position
            for marine in self.level.marines
            if marine is not exclude and marine.is_alive
        }
        other_routes = {
            cell
            for marine in self.level.marines
            if marine is not exclude
            for cell in marine.patrol_route
        }
        forbidden = snake_cells | occupied_marines | other_routes | set(self.level.safe_zone) | self.level.blocked_cells()
        reachable = self.level.reachable_cells(self.snake.segments[0])
        candidates = sorted(
            reachable - forbidden,
            key=lambda position: (
                abs(position.row - self.snake.segments[0].row) + abs(position.col - self.snake.segments[0].col),
                position.row,
                position.col,
            ),
            reverse=True,
        )

        valid = set(candidates)
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        for start in candidates:
            for delta_row, delta_col in directions:
                for length in (4, 3, 2):
                    route = tuple(
                        GridPosition(row=start.row + delta_row * offset, col=start.col + delta_col * offset)
                        for offset in range(length)
                    )
                    route_cells = set(route)
                    if route_cells.issubset(valid):
                        return route
        return None

    def _update_marine_patrols(self) -> None:
        for marine in self.level.marines:
            if not marine.is_alive or marine.state != "idle" or len(marine.patrol_route) < 2:
                continue

            marine.move_ticks += 1
            if marine.move_ticks < MARINE_MOVE_TICKS:
                continue
            marine.move_ticks = 0

            next_index = marine.route_index + marine.route_step
            if next_index >= len(marine.patrol_route) or next_index < 0:
                marine.route_step *= -1
                next_index = marine.route_index + marine.route_step

            next_position = marine.patrol_route[next_index]
            if next_position in self.snake.segments:
                continue

            next_direction = self._direction_between(marine.position, next_position)
            if next_direction is not None:
                marine.visual_direction = next_direction
            marine.route_index = next_index
            marine.position = next_position

    def _direction_between(self, start: GridPosition, end: GridPosition) -> Direction | None:
        delta = (end.row - start.row, end.col - start.col)
        for direction in Direction:
            if direction.delta == delta:
                return direction
        return None
