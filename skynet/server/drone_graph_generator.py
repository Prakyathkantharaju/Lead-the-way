# This file is generate a graph of the drone's commands and the drone images.

# First the commands are combined into a position using rotation and translation.
# Then the images are combined into a graph using the position.

# The graph is then saved to a file. (databases based on the poisition)
from typing import List
import numpy as np
from sqlite_helper import PickleSQLiteHelper
from dataclasses import dataclass
import networkx as nx

@dataclass
class Databases:
    """Class to hold the database names for the different types of data"""
    drone: str = 'databases/drone.db'
    save_graph: str = 'databases/drone_graph.db'



class Drone_graph_generator:
    def __init__(self, threshold_location: float = 0.1) -> None:
        self.threshold_location = threshold_location
        self.drone_db = PickleSQLiteHelper(Databases.drone)
        self._id = 0

    def _initialize_graph(self) -> None:
        self.graph = nx.Graph()
        self._node_number = 0
        # nodes will have the following attributes:
        #   image: the image of the node
        #   position: the position of the node
        #   commands: the commands of the node
        #   time: the time of the node
        # edges will have the following attributes:
        #   commands: the commands of the edge

    def build_graph(self, start_index: int|None = None, start_position: List[int]|None = None) -> None:
        if start_index is not None:
            self._id = start_index
        if start_position is not None:
            self._position = np.array([0, 0, 0])
        last_id = self.drone_db.get_count()
        while True:
            if self._id >= last_id:
                break
            self._build_graph()

    def _update_graph(self, image: np.array, position: np.array, commands: List[str], time: float, id: int) -> None:
        self.graph.add_node(self._node_number, image=image, position=position, commands=commands, time=time, id=id)
        if self._node_number > 0:
            self.graph.add_edge(self._node_number - 1, self._node_number, commands=commands)
        self._node_number += 1
        self._position = position

    def _smart_image_save(self, image: np.array, position: np.array) -> None:
        #TODO smart way to save select the best image to save
        pass 


    def _build_graph(self) -> None:
        # Get the commands
        #TODO test the image and time is correct
        image, commands, time = self.drone_db.retrieve_pickle(start_index=self._id)
        self._id += len(commands)
        # Combine the commands into a position
        position = self._combine_commands(commands, time)

        if (self._position - position > self.threshold_location).any():
            self._update_graph(image, position, commands, time, self._id)

        

    def _combine_commands(self, commands: List[str], time: float) -> np.array:
        cur_position = self._position
        # deal with translation
        # In the command the data is in the order of [x_vel , y_vel, z_vel, yaw_vel]
        cur_position += np.array([commands[0], commands[1], commands[2]]) * time #robot This can be done in the robot

        # deal with rotation
        cur_position = self._rotation_matrix(commands[3]) * cur_position #robot This can be done in the robot

        return cur_position

        
    def _rotation_matrix(self, yaw: float) -> np.array:
        # This is a 3D rotation matrix
        return np.array([[np.cos(yaw), -np.sin(yaw), 0],
                            [np.sin(yaw), np.cos(yaw), 0],
                            [0, 0, 1]])
    

