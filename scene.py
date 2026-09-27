from abc import ABC, abstractmethod

from simulation_object import SimulationObject
from vector2 import Vector2


class Scene(ABC):
    def __init__(self) -> None:
        self._root: Root = Root()

    @abstractmethod
    def load_scene(self) -> None:
        pass

    @property
    def root(self) -> Root:
        return self._root


class Root(SimulationObject):
    def __init__(
        self,
        position: Vector2 | None = None,
        *,
        active: bool = True,
        visible: bool = True
    ) -> None:
        super().__init__(self, position, active=active, visible=visible)

    @property
    def position(self) -> Vector2:
        return self._local_position

    @position.setter
    def position(self, position: Vector2) -> None:
        self._local_position = position