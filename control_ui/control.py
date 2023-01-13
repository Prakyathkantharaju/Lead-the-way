import abc



# abstract class
class Control(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError



