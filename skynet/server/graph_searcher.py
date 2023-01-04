import neo4j
from typing import List, Tuple, Dict, Any
import pandas as pd


class GraphSearcher:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._driver = neo4j.GraphDatabase.driver(
            self.config["location"],
            auth=(self.config["username"], self.config["password"]),
        )


    def close(self) -> None:
        self._driver.close()

    def search(self, start_location: List[float], end_location: List[float] ) -> pd.DataFrame:
        with self._driver.session(database=self.config["name"]) as session:
            return_value = session.execute_read(self._search, self.config["robot_name"], start_location, end_location)
        return return_value

    def _search(self, tx, robot_name:str , start_location: List[float], end_location: List[float]) -> pd.DataFrame:
        result = tx.run(
            "MATCH (a:$ROBOT {location: $}), (b:Robot) "
            "RETURN a, b ", ROBOT = robot_name, START_LOCATION = start_location, END_LOCATION = end_location)
        return result.to_df(expand=True)
        