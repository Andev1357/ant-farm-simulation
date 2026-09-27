from constants import SCRN_DIMS
from ant_farm_simulation.ant import Ant
from ant_farm_simulation.food_manager import FoodManager
from ant_farm_simulation.pheromone_field import PheromoneField
from ant_farm_simulation.ant_pheromone_dropper import AntPheromoneDropper
from scene import Scene
from vector2 import Vector2


class AntFarmScene(Scene):
    def load_scene(self) -> None:
        cell_size: Vector2 = Vector2(5, 5)
        self._home_field: PheromoneField = PheromoneField(self.root, cell_size=cell_size, evap_rate=0.9)
        self._food_field: PheromoneField = PheromoneField(self.root, cell_size=cell_size, evap_rate=0.7)

        self._food_manager: FoodManager = FoodManager(self.root, food_amount=5, starting_food=500, min_dist=200, max_dist=300)

        num_ants: int = 500
        ants: list[Ant] = []
        for _ in range(num_ants):
            center: Vector2 = SCRN_DIMS / 2
            ant: Ant = Ant(self.root, self._home_field, self._food_field, self._food_manager, center, speed=250)
            
            home_dropper: AntPheromoneDropper = AntPheromoneDropper(ant, ant, self._home_field, starting_strength=15, decay=0.5)
            food_dropper: AntPheromoneDropper = AntPheromoneDropper(ant, ant, self._food_field, starting_strength=15, decay=0.3)
            ant.set_droppers(home_dropper, food_dropper)

            ants.append(ant)
        
        
