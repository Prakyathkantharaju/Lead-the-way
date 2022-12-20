from abc import ABC, abstractmethod
import dataclasses



@dataclasses.dataclass
class command:
    left: str = "left"
    right: str = "right"
    forward: str = "forward"
    backward: str = "backward"
    stop: str = "stop"
class robot(ABC):

    def __init__(self, name, config):
        """
        Constructor for the robot class 
        """
        self.name = name
        self.config = config
        
    @abstractmethod
    def control(self):
        raise NotImplementedError

    @abstractmethod
    def get_state(self):
        raise NotImplementedError

    @abstractmethod
    def get_config(self):
        raise NotImplementedError

    @abstractmethod
    def add_graph(self):
        raise NotImplementedError 
