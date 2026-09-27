from typing import TypeVar, Generic

from simulation_object import SimulationObject

T = TypeVar('T', bound=SimulationObject)

class SimulationObjectReference(Generic[T]):
    def __init__(self, simulation_object: T) -> None:
        self._referenced_object: T | None = simulation_object

    def get(self) -> SimulationObject | None:
        if self._referenced_object is not None and self._referenced_object.destroyed:
            self._referenced_object = None
        return self._referenced_object

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SimulationObjectReference):
            return self._referenced_object is not None and self._referenced_object == other.get()
        elif isinstance(other, SimulationObject):
            return self._referenced_object == other
        raise TypeError(f"invalid equality comparison between {type(self)} and {type(other)}")

class SimulationObjectReferenceError(RuntimeError):
    def __init__(self, message: str = "") -> None:
        self.message: str = message
        super().__init__(self.message)