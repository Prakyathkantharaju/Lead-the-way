import numpy as np
import pickle
import torch
from efficientnet_pytorch import EfficientNet
import torchvision.transforms as transforms
from PIL import Image
import networkx as nx



class DiffCar(object):
    def __init__(self, config):
        self.config = config
        self.data_store = config['data_store']
        self.model = EfficientNet.from_pretrained('efficientnet-b0')
        self.tranformation = transforms.Compose([transforms.Resize(224), 
                                                 transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        self.cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        self.seed = 13648
        self.Graph = nx.Graph()

    def _get_features(self, image: np.ndarray) -> torch.Tensor:
        img = Image.fromarray(image)
        img_transformed = self.tranformation(img)
        im_vev = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
        return im_vev

    def _update_graph(self, features: torch.Tensor, data:dict, 
                      robot_name:str = "diff_car") -> None:
        id = self.Graph.number_of_nodes()
        self.Graph.add_node(id, features=features, location=data['location'],
                            image = data['image'])
        # if not starting node please add edge
        if self.Graph.number_of_nodes() > 1:
            self.Graph.add_edge(id, id - 1, robot_name=robot_name, 
                                command = data['command'],
                                speed = data['speed'])

    def processing_function(self, msg):
        # processing function
        data = pickle.loads(msg)
        image = data['image']
        # get features from the image
        features = self._get_features(image)
        self._update_graph(features, data)
        
