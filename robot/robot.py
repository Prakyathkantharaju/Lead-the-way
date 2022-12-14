from abc import ABC, abstractmethod

class robot(ABC):
        
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
