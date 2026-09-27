import time
import tkinter as tk
from time import perf_counter

from ant_farm_simulation.ant_farm_scene import AntFarmScene
from constants import SCRN_DIMS
from ant_farm_simulation.ant_farm_renderer import AntFarmRenderer
from renderer import Renderer
from simulation import Simulation


class Main:
    def __init__(self) -> None:
        self.profile_start: float = perf_counter()
        self.simulation_time: float = 0.0
        self.render_time: float = 0.0
        self._total_frame_time_ms = 0.0
        self._frame_count = 0    

        self.root: tk.Tk = tk.Tk()
        self.root.title("Simulation")

        self.canvas: tk.Canvas = tk.Canvas(
            self.root,
            width=SCRN_DIMS.x,
            height=SCRN_DIMS.y
        )
        self.canvas.pack()

        self.scene: AntFarmScene = AntFarmScene()
        self.renderer: Renderer = AntFarmRenderer(self.canvas, SCRN_DIMS)
        self.simulation: Simulation = Simulation(self.scene)

        self.last_time: float = time.perf_counter()
        self.run_simulation()

        self.root.mainloop()

    def run_simulation(self) -> None:
        current_time: float = time.perf_counter()
        dt: float = current_time - self.last_time
        self.last_time = current_time

        self.debug_update(dt)

        self.root.after(1, self.run_simulation)

    def update(self, dt: float) -> None:
        reps: int = 10
        for _ in range(reps):
            self.simulation.update(0.05)

        self.renderer.render(self.simulation)

    def debug_update(self, dt: float) -> None:
        reps: int = 5

        frame_start = perf_counter()

        start: float = perf_counter()
        for _ in range(reps):
            self.simulation.update(0.03)
        self.simulation_time += perf_counter() - start

        start = perf_counter()
        self.renderer.render(self.simulation)
        self.render_time += perf_counter() - start

        frame_time_ms = (perf_counter() - frame_start) * 1000
        self._total_frame_time_ms += frame_time_ms
        self._frame_count += 1

        elapsed = perf_counter() - self.profile_start
        if elapsed >= 1.0:
            simulation_percent = (self.simulation_time / elapsed) * 100
            render_percent = (self.render_time / elapsed) * 100
            avg_frame_time_ms = self._total_frame_time_ms / self._frame_count

            print(f"Over {elapsed:.1f}s:")
            print(f"  Simulation:       {simulation_percent:.1f}%")
            print(f"  Rendering:        {render_percent:.1f}%")
            print(f"  Other:            {100 - simulation_percent - render_percent:.1f}%")
            print(f"  Avg frame time:   {avg_frame_time_ms:.2f} ms")
            print(f"  Frame rate:       {1000 / avg_frame_time_ms:.1f} FPS")

            self.profile_start = perf_counter()
            self.simulation_time = 0.0
            self.render_time = 0.0
            self._total_frame_time_ms = 0.0
            self._frame_count = 0


if __name__ == "__main__":
    main: Main = Main()
