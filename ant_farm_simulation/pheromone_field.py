from simulation_object import SimulationObject
from constants import SCRN_DIMS
from vector2 import Vector2


class PheromoneField(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        position: Vector2 | None = None,
        cell_size: Vector2 | None = None,
        evap_rate: float = 0.1,
    ) -> None:
        super().__init__(parent, position)

        self._evap_rate: float = evap_rate
        self._cell_size: Vector2 = cell_size if cell_size is not None else Vector2(10, 10)

        self._generate_empty_grid()

    def _generate_empty_grid(self) -> None:
        self._grid: list[list[float]] = []
        self._grid_size: Vector2 = self._calculate_grid_size()

        self._grid = [[0.0 for _ in range(int(self._grid_size.y))] for _ in range(int(self._grid_size.x))]

    def _calculate_grid_size(self) -> Vector2:
        x: float = (SCRN_DIMS.x + self._cell_size.x * 2) // self._cell_size.x
        y: float = (SCRN_DIMS.y + self._cell_size.y * 2) // self._cell_size.y

        return Vector2(x, y)

    def _update(self, dt: float) -> None:
        self._evaporate_pheromones(dt)

    def _evaporate_pheromones(self, dt: float) -> None:
        for x in range(int(self._grid_size.x)):
            for y in range(int(self._grid_size.y)):
                if self._grid[x][y] != 0:
                    self._grid[x][y] *= (1 - ((1 - self._evap_rate) * dt))
                    self._grid[x][y] = max(0.0, self._grid[x][y])

    def add_at(self, grid_pos: Vector2, amount: float) -> None:
        if not self.in_range(grid_pos):
            return
        
        self._grid[int(grid_pos.x)][int(grid_pos.y)] = max(self._grid[int(grid_pos.x)][int(grid_pos.y)], amount)

    def get_at(self, grid_pos: Vector2) -> float:
        if not self.in_range(grid_pos):
            return 0.0
        
        return self._grid[int(grid_pos.x)][int(grid_pos.y)]

    def in_range(self, grid_pos) -> bool:
        return not (grid_pos.x < 0 or grid_pos.x >= len(self._grid) or grid_pos.y < 0 or grid_pos.y >= len(self._grid[0]))

    def world_to_grid(self, pos: Vector2) -> Vector2:
        return Vector2(
            int(round(pos.x / self._cell_size.x)),
            int(round(pos.y / self._cell_size.y)),
        )

    def grid_to_world(self, grid_pos: Vector2) -> Vector2:
        return Vector2(
            grid_pos.x * self._cell_size.x,
            grid_pos.y * self._cell_size.y,
        )

    def get_grid(self) -> list[list[float]]:
        return self._grid.copy()

    @property
    def cell_size(self) -> Vector2:
        return self._cell_size

    @property
    def grid_size(self) -> Vector2:
        return self._grid_size

    