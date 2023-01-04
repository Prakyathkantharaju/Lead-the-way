from typing import Dict, List, Any
import numpy.typing as npt
import pandas as pd

#neo4j based import
from neo4j import GraphDatabase



class GraphCreator: 
    """Create graph node and connection based on location and id
    """
    def __init__(self, config: Dict) -> None:
        """
        Initial the function to get the main class
        """
        self.db_location = config['location']
        self.db_name = config['name']
        self.username = config['username']
        self.password = config['password']
        self.Robot_type = config['Robot_type']
        self.driver = GraphDatabase.driver(f"bolt://localhost:7687", auth=(self.username, self.password))
        self._id  = int(0)

    def close(self) -> None:
        self.driver.close()

    def create_node(self, location: List, image: npt.ArrayLike) -> bool:
        with self.driver.session(database = self.db_name) as session:
            return_value = session.execute_write(self._create_node, 
                    location, image.to_bytes(), self._id) #type: ignore
        if return_value is None:
            return False
        else:
            self._id += 1
            return True

    def _create_node(self, tx, location: List, image: bytes, id: int) -> pd.DataFrame:
        print(type(tx))
        result = tx.run("CREATE (a:$ROBOT) "
                "SET a.id = $ID "
                "SET a.location = $LOCATION "
                "SET a.image = $IMAGE "
                "RETURN a",ROBOT=self.Robot_type, ID = id, 
                LOCATION = location, IMAGE = image)
        return result.to_df(extract = True)

    def setup_connection(self, start_location: List, end_location: List) -> pd.DataFrame:
        """Setup the connection between the nodes

        Args:
            start_location (List): [x,y,z] coordinate of the start location
            end_location (List): [x,y,z] coordinate of the end location

        Returns:
            pd.DataFrame: Return the value of the connection dataframe
        """
        with self.driver.session(database = self.db_name) as session:
            return_value = session.execute_write(self._setup_connection, 
                    start_location, end_location)
        return return_value

    def _setup_connection(self, tx, start_location: List, end_location: List) -> pd.DataFrame:
        result = tx.run("MATCH (a:$ROBOT {location: $START_LOCATION}), (b:$ROBOT {location: $END_LOCATION}) "
                "MERGE (a)-[r:CONNECTED]->(b) "
                "RETURN a, b, r", ROBOT= self.Robot_type, START_LOCATION = start_location, END_LOCATION = end_location)
        return result.to_df(extract = True)
    
    def setup_previous(self) -> bool:
        """Connect the previous node to the current node

        Returns:
            pd.DataFrame: of the new nodes.
        """
        # setup connection between the previous node and the current node.
        # based on the id 
        with self.driver.session(database = self.db_name) as session:
            return_value = session.execute_write(self._setup_previous, self._id)
        return return_value

    def _setup_previous(self, tx, id: int) -> pd.DataFrame:
        result = tx.run("MATCH (a:$ROBOT {id: $ID}), (b:$ROBOT {id: $ID - 1}) "
                "MERGE (a)-[r:PREVIOUS]->(b) "
                "RETURN a, b, r", ROBOT = self.Robot_type, ID = id)
        return result.to_df(extract = True)