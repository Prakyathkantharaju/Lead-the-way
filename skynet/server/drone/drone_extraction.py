from typing import Dict, List
import numpy.typing as npt
import pandas as pd

#neo4j based import
from neo4j import GraphDatabase



class Drone: 
    def __init__(self, config: Dict) -> None:
        """
        Initial the function to get the main class
        """
        self.db_location = config['location']
        self.db_name = config['name']
        self.username = config['username']
        self.password = config['password']
        self.driver = GraphDatabase.driver(f"bolt://localhost:7687", auth=(self.username, self.password))
        self._id  = int(0)

    def close(self) -> None:
        self.driver.close()

    def create_node(self, location: List, image: npt.ArrayLike, command: npt.ArrayLike) -> bool:
        with self.driver.session(database = self.db_name) as session:
            return_value = session.execute_write(self._create_node, 
                    location, image.to_bytes(), command.to_bytes(), self._id) #type: ignore
        if return_value is None:
            return False
        else:
            self._id += 1
            return True

    def _create_node(self, tx, location: List, image: bytes, command: bytes, id: int) -> pd.DataFrame:
        print(type(tx))
        result = tx.run("CREATE (a:Drone) "
                "SET a.id = $ID "
                "SET a.location = $LOCATION "
                "SET a.image = $IMAGE "
                "SET a.command = $COMMAND "
                "RETURN a", ID = id, 
                LOCATION = location, COMMAND = command, IMAGE = image)
        return result.to_df(extract = True)

    def setup_connection(self, start_location: List, end_location: List) -> bool|Any:
        #TODO search the database for the location and connect the database.
        return 0
    
    def setup_previous(self) -> bool:
        # setup connection between the previous node and the current node.
        # based on the id 
        return 0

    def 
        
