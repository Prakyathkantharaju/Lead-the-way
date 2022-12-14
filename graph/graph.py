from abc import ABC, abstractmethod

class graph(ABC):
    
    @abstractmethod
    def add_info(self):
        raise NotImplementedError


    @abstractmethod
    def add_edge(self):
        raise NotImplementedError

    @abstractmethod
    def add_node(self):
        raise NotImplementedError

    