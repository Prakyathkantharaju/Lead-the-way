from ..robot import Robot

class Drone(Robot):
    def __init__(self, config: dict) -> None:
        super().__init__() # Call the parent class constructor
        self._name = config['name']
        self._graph_rate = config['graph_rate']
        self._graph_config = config['graph_config']
        self._image_processing = config['image_processing']


    def run(self) -> None:
        print("Drone is running")