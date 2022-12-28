from neo4j import GraphDatabase
import numpy as np

# graph = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Skynet"))


class Drone:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Skynet"))
        self._id = int(0)

    def close(self):
        self.driver.close()


    def create_print_node(self, location, image, command):
        with self.driver.session(database="Drone2") as session:
            greeting = session.execute_write(self._create_nodes, location.tolist(), image.tobytes(), command.tobytes(), self._id)
            self._id += 1
            print(self._id)

        if self._id > 1:
            with self.driver.session(database="Drone2") as session:
                greeting = session.execute_write(self._create_relationships, self._id)
    
    def get_last_node(self):
        with self.driver.session(database="Drone2") as session:
            greeting = session.execute_read(self._get_last_node)
            self._id = greeting
        return greeting

    def get_node_by_location(self, start_location, end_location):
        with self.driver.session(database="Drone2") as session:
            node_information = session.execute_read(self._get_node_by_location, start_location, end_location)
        return node_information

    def _get_node_by_location(self, tx, start_location, end_location):
        print(start_location, end_location)
        result = tx.run("MATCH (n:Drone) "
        "WHERE n.location > $start_location AND n.location < $end_location "
        "RETURN * ", start_location=start_location, end_location=end_location)
        return result.to_df(expand=True)

    def _get_last_node(self, tx):
        result = tx.run("Match (n) "
                        "Return n.id "
                        "Order by n.id desc ")
        print(result.single()[0])
        
        if type(result.single()) is type(None):
            return 0
        else:
            return result.single()[0]
    @staticmethod
    def _create_nodes(tx, location, image, command, id):
        result = tx.run("CREATE (a:Drone) "
                        "SET a.id = $id  "
                        "SET a.location = $location "
                        "SET a.image = $image "
                        "SET a.command = $command "
                        "RETURN id(a)", id=id, location=location, image=image, command=command)
        if result.single() is None:
            return 0
        else:
            return result.single()

    @staticmethod
    def _create_relationships(tx, id):
        result = tx.run("MATCH (a:Drone), (b:Drone) "
                        "WHERE a.id = $prev_id AND b.id = $next_id "
                        "CREATE (a)-[r:Next]->(b) "
                        "RETURN type(r)", prev_id=id-1, next_id=id)


if __name__ == "__main__":
    greeter = Drone()
    greeter.get_last_node()
    # for i in range(10):
        # greeter.create_print_node(np.array([i, i, i]), np.random.rand(3, 3), np.random.rand(3))
    greeter.get_node_by_location([10], [5]*3)

    greeter.close()