import numpy as np
import pickle
import torch
from efficientnet_pytorch import EfficientNet
import torchvision.transforms as transforms
# from PIL import Image
import networkx as nx

# local
from sqlite_helper import PickleSQLiteHelper



class DiffCar(object):
    def __init__(self, config) -> None:
        self.config = config
        self.data_store = config['data_store']
        self.model = EfficientNet.from_pretrained('efficientnet-b0')
        self.tranformation = transforms.Compose([transforms.Resize(224), 
                                                 transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        self.cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        self.seed = 13648
        self.Graph = nx.Graph()
        self.db = PickleSQLiteHelper(self.data_store)
        self.db.create_table('diff_car')
        self.counter = self.db.get_count()
        if self.counter is None:
            self.counter = 0

    # def _get_features(self, image: np.ndarray) -> torch.Tensor:
    #     img = Image.fromarray(image)
    #     img_transformed = self.tranformation(img)
    #     im_vev = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
    #     return im_vev

    def _update_graph(self, data:dict, 
                      robot_name:str = "diff_car") -> None:
        id = self.Graph.number_of_nodes()
        self.Graph.add_node(id,location=data['location'], 
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
        graph_pickle = pickle.dumps(self.Graph)
        if self.counter is None:
            self.counter = 0
        updated_counter = self.db.insert_pickle('diff_car', self.counter+1, 
                            data['image'], data['location'] + data['time'], 
                              graph_pickle)
        self.counter = updated_counter
        
