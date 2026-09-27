import math
import random

from constants import SCRN_DIMS
from simulation_object import SimulationObject, SimulationObjectReference
from vector2 import Vector2
from ant_farm_simulation.food import Food


class FoodManager(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        position: Vector2 | None = None,
        *,
        food_amount: int = 5,
        starting_food: int = 500,
        min_dist: float = 200,
        max_dist: float = 400,
    ) -> None:
        super().__init__(parent, position)

        self._max_food: int = food_amount
        self._starting_food: int = starting_food
        self._min_dist = min_dist
        self._max_dist = max_dist

        self._food_list: list[SimulationObjectReference[Food]] = []
        
        for _ in range(self._max_food):
            self.spawn_food()

    def spawn_food(self) -> None:
        distance: float = random.uniform(self._min_dist, self._max_dist)
        angle: float = random.uniform(0, 2 * math.pi)

        pos: Vector2 = SCRN_DIMS / 2 + Vector2(math.sin(angle), math.cos(angle)) * distance

        food: Food = Food(self, pos, starting_food=self._starting_food)

        self._food_list.append(SimulationObjectReference(food))

    def get_food(self) -> list[Food]:
        self._food_list = [ref for ref in self._food_list if ref.get() is not None]
        return [food for ref in self._food_list if (food := ref.get()) is not None]