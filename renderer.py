import tkinter as tk
from abc import ABC, abstractmethod

from simulation import Simulation
from simulation_object import SimulationObject
from vector2 import Vector2
from color import Color


class Renderer(ABC):
    DEFAULT_TAG: str = "default"

    def __init__(self, canvas: tk.Canvas, scrn_dims: Vector2) -> None:
        self._canvas: tk.Canvas = canvas
        self._scrn_dims: Vector2 = scrn_dims

    def render(self, simulation: Simulation) -> None:
        self._canvas.delete(Renderer.DEFAULT_TAG)

        for child in simulation.scene.root.recursive_children:
            self._render_object(child)

    @abstractmethod
    def _render_object(self, obj: SimulationObject) -> None:
        pass

    def _render_circle(
        self,
        center: Vector2,
        radius: float,
        color: Color,
        *,
        outline: str | Color = "",
        tags: str | None = None
    ) -> None:
        self._canvas.create_oval(
            center.x - radius,
            center.y - radius,
            center.x + radius,
            center.y + radius,
            fill=str(color),
            tags=tags if tags is not None else Renderer.DEFAULT_TAG,
            outline=str(outline),
        )