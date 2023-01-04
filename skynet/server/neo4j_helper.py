
# this is a protocol file for neo4j
# Path: skynet/server/neo4j_helper.py

import neo4j
from typing import List, Tuple, Dict, Any, Protocol
import pandas as pd

class Neo4jGraphCreator(Protocol):
    def close(self):
        ...

    def create_node(self, location: List, image: bytes, command: bytes) -> pd.DataFrame:
        ...

    def setup_connection(self) -> pd.DataFrame:
        ...

    def close(self) -> None:
        ...

    def setup_previous(self) -> pd.DataFrame:
        ...

class Neo4jgraphSearch(Protocol):
    def close(self) -> None:
        ...

    def search(self, start_location: List[float], end_location: List[float]) -> pd.DataFrame:
        ...