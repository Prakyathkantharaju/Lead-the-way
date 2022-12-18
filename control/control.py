import pygame as pg
import abc



# abstract class
class Control(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError


    @abc.abstractmethod
    def process_event(self, event):
        raise NotImplementedError

