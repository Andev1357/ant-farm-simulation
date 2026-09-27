from simulation_object import SimulationObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ant_farm_simulation.ant import Ant
    from ant_farm_simulation.pheromone_field import PheromoneField


class AntPheromoneDropper(SimulationObject):
    def __init__(
        self,
        parent: SimulationObject,
        ant: Ant,
        field: PheromoneField,
        *,
        starting_strength: float,
        decay: float
    ) -> None:
        super().__init__(parent)

        self._ant: Ant = ant
        self._field: PheromoneField = field
        self._start_strength: float = starting_strength
        self._decay: float = decay

        self._current_strength: float = starting_strength

    def reset_strength(self) -> None:
        self._current_strength = self._start_strength

    def _update(self, dt: float) -> None:
        self._current_strength *= (1 - ((1 - self._decay) * dt))
        self._field.add_at(self._field.world_to_grid(self.position), self._current_strength)