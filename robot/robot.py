from abc import ABC, abstractmethod

class robot(ABC):
    def __init__(self, config: dict) -> None:
        self.config = config
        
    @abstractmethod
    def control(self, control: dict) -> dict:
        state = {}
        return state

    @abstractmethod
    def get_state(self) -> dict:
        state = {}
        return state

    @abstractmethod
    def get_config(self) -> dict:
        return self.config

    @abstractmethod
    def get_graph(self) -> dict:
        graph = {}
        return graph 
