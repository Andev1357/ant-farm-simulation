import tkinter as tk
from PIL import Image, ImageTk

from ant_farm_simulation.pheromone_field import PheromoneField
from ant_farm_simulation.ant import Ant
from ant_farm_simulation.food import Food
from simulation import Simulation
from simulation_object import SimulationObject
from renderer import Renderer
from vector2 import Vector2
from color import Color
from constants import SCRN_WIDTH, SCRN_HEIGHT

class AntFarmRenderer(Renderer):
    PHEROMONE_TAG = "pheromone"
    PHEROMONE_UPDATE_INTERVAL = 3

    def __init__(self, canvas: tk.Canvas, scrn_dims: Vector2) -> None:
        super().__init__(canvas, scrn_dims)

        self._frame_counter = 0
        self._pheromone_field_index = 0
    
        self._pheromone_images: list[Image.Image] = []
        self._pheromone_photos: list[ImageTk.PhotoImage] = []
        self._pheromone_canvas_items: list[int] = []

    def render(self, simulation: Simulation) -> None:
        self._ant_count = 0
        self._pheromone_field_index = 0

        super().render(simulation)

        self._render_circle(self._scrn_dims / 2, 20, Color(219, 112, 76), outline=Color(0, 0, 0))

        self._frame_counter = (self._frame_counter + 1) % self.PHEROMONE_UPDATE_INTERVAL

    def _render_object(self, obj: SimulationObject) -> None:
        if isinstance(obj, Ant):
            self._render_ant(obj)
        elif isinstance(obj, Food):
            self._render_food(obj)
        elif isinstance(obj, PheromoneField):
            if self._frame_counter == 0:
                self._render_pheromones(obj)

    def _render_pheromones(self, pheromone_field: PheromoneField) -> None:
        grid: list[list[float]] = pheromone_field.get_grid()

        height: int = len(grid)
        width: int = len(grid[0])
        index: int = self._pheromone_field_index

        if index >= len(self._pheromone_images):
            image: Image.Image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            self._pheromone_images.append(image)
        else:
            image = self._pheromone_images[index]

        pixels = image.load()
        if pixels is None: return

        color: Color = (
            Color(0, 0, 255)
            if index == 0
            else Color(255, 0, 0)
        )

        for x, values in enumerate(grid):
            for y, value in enumerate(values):
                intensity = max(0, min(255, int(value*17)))

                pixels[x, y] = (color.r, color.g, color.b, intensity)

        image = image.resize(
            (SCRN_WIDTH, SCRN_HEIGHT),
            Image.Resampling.NEAREST
        )

        photo: ImageTk.PhotoImage = ImageTk.PhotoImage(image)

        if index >= len(self._pheromone_photos):
            canvas_item = self._canvas.create_image(0, 0, image=photo, anchor=tk.NW, tags=self.PHEROMONE_TAG)
            self._pheromone_photos.append(photo)
            self._pheromone_canvas_items.append(canvas_item)
        else:
            self._pheromone_photos[index] = photo
            self._canvas.itemconfigure(self._pheromone_canvas_items[index], image=photo)

        self._pheromone_field_index += 1

    def _render_ant(self, ant: Ant) -> None:
        self._render_circle(ant.position, 2, Color(0, 0, 0))

    def _render_food(self, food: Food) -> None:
        self._render_circle(food.position, food.get_remaining() / 50, Color(255, 255, 0), outline=Color(0, 0, 0))
