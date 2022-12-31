
# this is a protocol file for neo4j
# Path: skynet/server/neo4j_helper.py

import neo4j
from typing import List, Tuple, Dict, Any, Protocol


class Neo4jAddition(Protocol):
    def close(self) -> None:
        ...

    def create_node(self, location: List, image: bytes, command: bytes) -> None:
        ...

    def setup_connection(self) -> None:
        ...

class Neo4jRetrieval(Protocol):
    def close(self) -> None:
        ...

    def get_last_node(self) -> int:
        ...

    def get_node_by_location(self, start_location: int, end_location: int) -> neo4j.Record:
        ...
