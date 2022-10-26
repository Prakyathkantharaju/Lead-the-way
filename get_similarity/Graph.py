

import numpy as np
import numpy.typing as npt
import cv2
from PIL import Image
import random
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from tqdm import tqdm
import networkx as nx
from efficientnet_pytorch import EfficientNet

from typing import Tuple, List

import warnings
warnings.filterwarnings("ignore")


class Graph_structure(object):

    def __init__(self, threshold: float = 0.5) -> None:
        self.Graph = nx.Graph()
        self.model = EfficientNet.from_pretrained("efficientnet-b0")
        self.model.to("cuda")
        self.cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        self.tranformation = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])
        self.seed = 13648
        self.N_images = 3
        self.images = ()
        self.features = []

    def _get_three_images(self, img: npt.ArrayLike) ->  Tuple:
        dim = img.shape[0]
        return (img[:,:dim // 3, :], img[:, dim//3 :dim*2//3, :], img[:,-dim//3:, :])

    def _get_features(self, image: npt.ArrayLike) -> None:
        img = Image.fromarray(image)
        img_transformed = self.tranformation(img).unsqueeze(0).to("cuda")
        im_vec = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
        return im_vec
 
    def add_images(self, img: npt.ArrayLike, X_Y_R: List[float] ) -> float:
        self.images = self._get_three_images(img)
        self._process_images(X_Y_R)

    def _add_node(self, number: int, features: npt.ArrayLike) -> None:
        self.Graph.add_node(number, features = features)

    def _add_initial_nodes(self):
        self.features = []
        self.central_nodes = 0
        number = self.Graph.number_of_nodes()
        nodes_add = []
        for i in range(3):
            self.features.append(self._get_features(self.images[i]))
            if i == 1:
                self.central_nodes = number  + i
            self._add_node(number + i, self.features[-1])
            nodes_add.append(number + i)

        # adding edges to the nodes
        self.Graph.add_edge(nodes_add[0], nodes_add[1], weight = 0.1, direction = '-1', distance = [])
        self.Graph.add_edge(nodes_add[1], nodes_add[2], weight = 0.1, direction = '1', distance = [])

    def _find_root_edge(self, X_Y_R: List[float], threshold: float  = 0.5):
        number = self.Graph.number_of_nodes()
        n = self._match_root_nodes(self.features[1], threshold = 0.5, top_threshold = number - 3, bottom_threshold = number - 6)
        assert n != -1
        weight = np.sqrt( (X_Y_R[0] * X_Y_R[2]) ** 2 + X_Y_R[1] ** 2)
        self.Graph.add_edge(n, self.central_nodes, weight = weight, direction = 0, distance = X_Y_R)
    
    def _match_root_nodes(self, features, threshold, top_threshold, bottom_threshold):
        feature_dict = nx.get_node_attributes(self.Graph, "features")
        values  = {}
        for key, value in feature_dict.items():
            if key > bottom_threshold and key < top_threshold:
                v = self.cos(features, value)
                values[key] = v
        return max(values, key=values.get)

            
        

    def _process_images(self, X_Y_R: List[float] ) -> None:
        if self.Graph.number_of_nodes() == 0:
            self._add_initial_nodes()
        else:
            self._add_initial_nodes()
            assert len(self.features) == 3
            self._find_root_edge(X_Y_R)


if __name__ == "__main__":
    G = Graph_data()
    cam = cv2.VideoCapture("../video/round_path.mp4")
    for i in tqdm(range(400)):
        if i % 15 != 0:
            continue
        SUCCESS, frame = cam.read()

        G.add_images(frame, [1,0,0])


    fig, ax = plt.subplots(1,1)
    nx.draw(G.Graph, ax = ax, with_labels = True)

    plt.show()
