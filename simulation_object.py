from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from vector2 import Vector2


class SimulationObject(ABC):
    def __init__(
        self,
        parent: SimulationObject, 
        position: Vector2 | None = None,
        *,
        active: bool = True,
        visible: bool = True
    ) -> None:
        self._parent: SimulationObjectReference = SimulationObjectReference(parent)
        self._local_position: Vector2 = position.copy() if position is not None else Vector2()
        self._active: bool = active
        self._visible: bool = visible
        self._destroyed: bool = False

        self._children: list[SimulationObjectReference] = []

        parent.add_child(self)

    def update(self, dt: float) -> None:
        if not self._active: 
            return
        
        self._update(dt)

        for child in self.children:
            child.update(dt)

    def _update(self, dt: float) -> None:
        pass

    def destroy(self) -> None:
        self._destroyed = True
        self._active = False
        self._visible = False
        for child in self.children:
            child.destroy()
        self._children = []

    def add_child(self, child: SimulationObject) -> None:
        if child in self._children or child is self:
            return
        self._children.append(SimulationObjectReference(child))

    @property
    def children(self) -> list[SimulationObject]:
        self._children = [ref for ref in self._children if ref.get() is not None]
        return [child for ref in self._children if (child := ref.get()) is not None]

    @property
    def recursive_children(self) -> list[SimulationObject]:
        result = []

        for child in self.children:
            result.append(child)
            result.extend(child.recursive_children)

        return result

    @property
    def parent(self) -> SimulationObject:
        if (parent := self._parent.get()) is None:
            raise SimulationObjectReferenceError("missing parent reference")
        return parent
    
    @property
    def position(self) -> Vector2:
        return self.parent.position + self._local_position

    @position.setter
    def position(self, position: Vector2) -> None:
        local_position = position - self.parent.position
        self._local_position = local_position

    @property   
    def local_position(self) -> Vector2:
        return self._local_position.copy()

    @local_position.setter
    def local_position(self, position: Vector2) -> None:
        self._local_position = position.copy()

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        self._visible = visible

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        self._active = active

    @property
    def destroyed(self) -> bool:
        return self._destroyed


T = TypeVar('T', bound=SimulationObject)

class SimulationObjectReference(Generic[T]):
    def __init__(self, simulation_object: T | None) -> None:
        self._referenced_object: T | None = simulation_object

    def get(self) -> T | None:
        if self._referenced_object is not None and self._referenced_object.destroyed:
            self._referenced_object = None
        return self._referenced_object

class SimulationObjectReferenceError(RuntimeError):
    def __init__(self, message: str = "") -> None:
        self.message: str = message
        super().__init__(self.message)