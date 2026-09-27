from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing import get_context, shared_memory
import random

import numpy as np
from numpy.typing import NDArray
from numpy import float32

from simulation_object import SimulationObject
from vector2 import Vector2

from ant_farm_simulation.ant import Ant
from ant_farm_simulation.pheromone_field import PheromoneField


@dataclass
class AntDirectionState:
    position: Vector2
    has_food: bool
    cell_size: Vector2


_home_grid: NDArray[np.float32] | None = None
_food_grid: NDArray[np.float32] | None = None
_home_shm: shared_memory.SharedMemory | None = None
_food_shm: shared_memory.SharedMemory | None = None


def _init_worker(
    home_shm_name: str,
    home_shape: tuple[int, int],
    food_shm_name: str,
    food_shape: tuple[int, int],
) -> None:
    global _home_grid
    global _food_grid
    global _home_shm
    global _food_shm

    _home_shm = shared_memory.SharedMemory(name=home_shm_name)
    _food_shm = shared_memory.SharedMemory(name=food_shm_name)

    _home_grid = np.ndarray(
        home_shape,
        dtype=np.float32,
        buffer=_home_shm.buf,
    )

    _food_grid = np.ndarray(
        food_shape,
        dtype=np.float32,
        buffer=_food_shm.buf,
    )

    if _home_grid is None or _food_grid is None:
        return
    _home_grid.flags.writeable = False
    _food_grid.flags.writeable = False


DIRECTIONS: tuple[Vector2, ...] = (
    Vector2(1, 0),
    Vector2(1, 1).normalised(),
    Vector2(0, 1),
    Vector2(-1, 1).normalised(),
    Vector2(-1, 0),
    Vector2(-1, -1).normalised(),
    Vector2(0, -1),
    Vector2(1, -1).normalised(),
)


def calculate_ant_direction(state: AntDirectionState) -> Vector2:
    field: NDArray[float32] | None = _home_grid if state.has_food else _food_grid

    if field is None:
        raise RuntimeError("pheromone grid has not been initialised")

    sensor_reach = 10
    sensitivity = 5

    strengths = []
    for direction in DIRECTIONS:
        position = state.position + direction * sensor_reach
        grid_pos = Vector2(position.x / state.cell_size.x, position.y / state.cell_size.y)
        strength = field[int(round(grid_pos.x))][int(round(grid_pos.y))] * sensitivity
        strengths.append(strength)

    weights: list[float] = [
        max(0.01, 0.01 + strength)
        for strength in strengths
    ]

    return random.choices(DIRECTIONS, weights=weights, k=1)[0]


class ParallelAntProcessor(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        ants: list[Ant],
        home_field: PheromoneField,
        food_field: PheromoneField,
        *,
        max_workers: int | None = None,
    ) -> None:
        super().__init__(parent)

        self._ants: list[Ant] = ants
        self._home_field: PheromoneField = home_field
        self._food_field: PheromoneField = food_field

        home_grid = self._home_field.get_grid()
        food_grid = self._food_field.get_grid()

        self._home_shm: shared_memory.SharedMemory = self._create_shared_grid(home_grid)
        self._food_shm: shared_memory.SharedMemory = self._create_shared_grid(food_grid)
        self._home_shape: tuple[int, int] = (len(home_grid), len(home_grid[0]))
        self._food_shape: tuple[int, int] = (len(food_grid), len(food_grid[0]))

        self._executor: ProcessPoolExecutor = ProcessPoolExecutor(
            max_workers=max_workers,
            mp_context=get_context("spawn"),
            initializer=_init_worker,
            initargs=(
                self._home_shm.name,
                self._home_shape,
                self._food_shm.name,
                self._food_shape,
            ),
        )

    @staticmethod
    def _create_shared_grid(grid: list[list[float]]) -> shared_memory.SharedMemory:
        array: NDArray[np.float32] = np.asarray(grid, dtype=np.float32)

        shm: shared_memory.SharedMemory = shared_memory.SharedMemory(create=True, size=array.nbytes)

        shared_array: NDArray[np.float32] = np.ndarray(array.shape, dtype=np.float32, buffer=shm.buf)

        shared_array[:] = array

        return shm

    @staticmethod
    def _update_shared_grid(shm: shared_memory.SharedMemory, grid: list[list[float]]) -> None:
        array: NDArray[np.float32] = np.asarray(grid, dtype=np.float32)

        shared_array: NDArray[np.float32] = np.ndarray(array.shape, dtype=np.float32, buffer=shm.buf)

        shared_array[:] = array

    def _update(self, dt: float) -> None:
        if not self._ants:
            return

        self._update_shared_grid(self._home_shm, self._home_field.get_grid())
        self._update_shared_grid(self._food_shm, self._food_field.get_grid())

        states: list[AntDirectionState] = [
            AntDirectionState(
                position=ant.position,
                has_food=ant.has_food,
                cell_size=ant._home_field.cell_size #TODO
            )
            for ant in self._ants
        ]

        results = self._executor.map(calculate_ant_direction, states)

        for ant, direction in zip(self._ants, results):
            ant.set_direction(direction)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=True)

        self._home_shm.close()
        self._food_shm.close()

        self._home_shm.unlink()
        self._food_shm.unlink()

    def __enter__(self) -> ParallelAntProcessor:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        self.shutdown()
