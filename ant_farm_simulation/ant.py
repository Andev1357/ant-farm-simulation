import random

from simulation_object import SimulationObject, SimulationObjectReference
from vector2 import Vector2
from constants import SCRN_DIMS

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ant_farm_simulation.ant_pheromone_dropper import AntPheromoneDropper
    from ant_farm_simulation.pheromone_field import PheromoneField
    from ant_farm_simulation.food_manager import FoodManager


class Ant(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        home_field: PheromoneField,
        food_field: PheromoneField,
        food_manager: FoodManager,
        position: Vector2 | None = None,
        *,
        speed: float = 25.0,
    ) -> None:
        super().__init__(parent, position)

        self._home_field: PheromoneField = home_field
        self._food_field: PheromoneField = food_field
        self._food_manager: FoodManager = food_manager

        self._start_pos: Vector2 = self.position.copy()

        self._speed: float = speed
        self._direction: Vector2 = Vector2()

        self._has_food: bool = False

        self._home_dropper: SimulationObjectReference[AntPheromoneDropper] = SimulationObjectReference(None)
        self._food_dropper: SimulationObjectReference[AntPheromoneDropper] = SimulationObjectReference(None)

    def set_droppers(self, home_dropper: AntPheromoneDropper, food_dropper: AntPheromoneDropper) -> None:
        self._home_dropper = SimulationObjectReference(home_dropper)
        self._food_dropper = SimulationObjectReference(food_dropper)
        self._update_droppers()

    def _update(self, dt: float) -> None:
        self._update_direction(dt)
        self._move(dt)

        self._check_for_home()
        self._check_for_food()

    def _check_for_home(self) -> None:
        if (self.position - self._start_pos).sqrmagnitude < 100:
            self._has_food = False
            self._update_droppers()

    def _check_for_food(self) -> None:
        for food in self._food_manager.get_food():
            if (self.position - food.position).sqrmagnitude < 100:
                if not self._has_food:
                    food.eat()
                    self._has_food = True
                self._update_droppers()

    def _update_droppers(self) -> None:
        if (food_dropper := self._food_dropper.get()) is not None:
            food_dropper.active = self._has_food
            food_dropper.reset_strength()
        if (home_dropper := self._home_dropper.get()) is not None:
            home_dropper.active = not self._has_food
            home_dropper.reset_strength()

    def _move(self, dt: float) -> None:
        move_vector: Vector2 = self._direction * (self._speed * dt)
        self.position += move_vector
        self.position = self.position.clamp(Vector2(), SCRN_DIMS)

    DIRECTIONS: list[Vector2] = [
        Vector2(1, 0),
        Vector2(1, 1).normalised(),
        Vector2(0, 1),
        Vector2(-1, 1).normalised(),
        Vector2(-1, 0),
        Vector2(-1, -1).normalised(),
        Vector2(0, -1),
        Vector2(1, -1).normalised(),
    ]

    def _update_direction(self, dt: float) -> None:
        field = (self._home_field if self._has_food else self._food_field)

        sensor_reach = 10
        sensitivity = 5
        strengths: list[float] = [
            field.get_at(field.world_to_grid(self.position + direction * sensor_reach)) * sensitivity 
            for direction
            in Ant.DIRECTIONS
        ]

        weights: list[float] = [max(0.01, 0.01+strength) for strength in strengths]

        self._direction = random.choices(self.DIRECTIONS, weights=weights)[0]

    def set_direction(self, direction: Vector2) -> None:
        self._direction = direction

    @property
    def has_food(self) -> bool:
        return self._has_food
