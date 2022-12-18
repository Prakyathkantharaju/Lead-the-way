from abc import ABC, abstractmethod

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
