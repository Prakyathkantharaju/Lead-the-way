from typing import Dict, List, Any
import numpy.typing as npt
import pandas as pd
import time

#neo4j based import
from skynet.server.graph_creator import GraphCreator
from skynet.server.sqlite_helper import PickleSQLiteHelper
from skynet.server.graph_searcher import GraphSearcher

# import for typing
from skynet.server.neo4j_helper import Neo4jGraphCreator, Neo4jgraphSearch

graph_config = {
    "location": "bolt://localhost:7687",
    "name": "skynet",
    "username": "neo4j",
    "password": "Skynet",
    "Robot_type": "Drone"
}

extractor_config = {
    "location": "databases/drone.db",
    "table_name": "drone"
}
raspberry

class Drone: 
    """Class to extract the drone data from the database
    and add to the database
    """
    def __init__(self) -> None:
        self.graph_generator: Neo4jGraphCreator = GraphCreator(graph_config)
        self.graph_search:Neo4jgraphSearch  = GraphSearcher(graph_config)
        self.config = extractor_config
        self.extractor = PickleSQLiteHelper(self.config["location"])
        
        self._prepare_extractor()

    def _prepare_extractor(self) -> None:
        """Prepare the extractor to extract the data
        """
        self._final_id = self.extractor.get_count
        self.extractor.commit()

    def run(self) -> None:
        """Run the function to extract the data from the database
        """
        run_id = 1
        while True:
            if run_id > self._final_id:
                time.sleep(3)
                print("no new data in the database.")
            self._extract_data(run_id)
            run_id += 1
            image, location,_=   self.extractor.retrieve_data(self.config['table_name'], run_id)
            

    def _graph_logic(self, image: npt.NDArray[Any], location: List[float]) -> None:
        """Add the data to the graph
        """
        # get approaximate location graphs
        start_location = [c - 1 for c in location]
        end_location = [c + 1 for c in location]
        nodes = self.graph_generator.search(start_location, end_location)
        if len(nodes) == 0:
            # create new node
            self.graph_generator.create_node(location, image)
            if self.graph_generator._id > 1:
                self.graph_generator.setup_previous()

        else:
            # Should I update the node? Note yet decided.
            pass
