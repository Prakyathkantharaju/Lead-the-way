import pickle
import networkx as nx

# local
from sqlite_helper import PickleSQLiteHelper

class Drone:
    def __init__(self, config) -> None:
        self.config = config
        self.data_store = config['data_store']
        self.seed = 13648
        self.Graph = nx.Graph()
        self.db = PickleSQLiteHelper(self.data_store)
        self.db.create_table('drone')
        self.counter = self.db.get_count()
        if self.counter is None:
            self.counter = 0

    # def _get_features(self, image: np.ndarray) -> torch.Tensor:
    #     img = Image.fromarray(image[np.newaxis,:])
    #     img_transformed = self.tranformation(img)
    #     im_vev = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
    #     return im_vev

    def _update_graph(self, data:dict,
                      robot_name:str = "drone") -> None:
        id = self.Graph.number_of_nodes()
        self.Graph.add_node(id, location=data['location'],
                            image = data['img'], time = data['time'])
        # if not starting node please add edge
        if self.Graph.number_of_nodes() > 1:
            self.Graph.add_edge(id, id - 1, robot_name=robot_name,
                                command = data['command'],
                                speed = data['speed'])
    

    def process_function(self, msg):
        # processing function
        data = pickle.loads(msg)
        # get features from the image
        # features = self._get_features(image)
        self._update_graph(data)
        print(f"Counter {self.counter}")
        graph_pickle = pickle.dumps(self.Graph)
        if self.counter is None:
            self.counter = 0
        updated_counter = self.db.insert_pickle('drone', self.counter+1, 
                            data['img'], data['location'], data['time'], 
                              graph_pickle)
        self.counter = updated_counter
        print(self.counter)




