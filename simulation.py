from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scene import Scene


class Simulation:
    def __init__(self, scene: Scene) -> None:
        self._scene: Scene = scene
        self._scene.load_scene()

    def update(self, dt: float) -> None:
        self._scene.root.update(dt)

    @property
    def scene(self) -> Scene:
        return self._scene
