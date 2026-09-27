from simulation_object import SimulationObject
from vector2 import Vector2

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ant_farm_simulation.food_manager import FoodManager


class Food(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        position: Vector2 | None = None,
        *,
        starting_food: int = 100
    ) -> None:
        super().__init__(parent, position)

        self.remaining: int = starting_food

    def eat(self) -> None:
        self.remaining -= 1

        if self.remaining <= 0:
            self.destroy()

    def get_remaining(self) -> int:
        return self.remaining