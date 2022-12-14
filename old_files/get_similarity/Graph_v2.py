

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
import copy

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
        self.node_number = 1


    def _get_features(self, image: npt.ArrayLike) -> None:
        img = Image.fromarray(image)
        img_transformed = self.tranformation(img).unsqueeze(0).to("cuda")
        im_vec = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
        return im_vec
 
    def add_images(self, img: npt.ArrayLike, X_Y_R: List[float] ) -> float:
        self.images = img
        self._process_images(X_Y_R)

    def _add_node(self, number: int, features: npt.ArrayLike, images = npt.ArrayLike) -> None:
        self.Graph.add_node(number, features = features, images = images)

    def _add_initial_nodes(self):
        self.features = []
        number = self.node_number
        features = self._get_features(self.images)
        self._add_node(number + 1, features, self.images)

        # update the node number
        self.node_number += 1

    def _find_root_edge(self, X_Y_R: List[float], threshold: float  = 0.5):
        number = self.node_number
        weight = np.sqrt( (X_Y_R[0] * X_Y_R[2]) ** 2 + X_Y_R[1] ** 2)
        self.Graph.add_edge(number, number - 1, weight = weight, direction = 0, distance = copy.copy(X_Y_R))
    

    def _process_images(self, X_Y_R: List[float]) -> None:
        if self.Graph.number_of_nodes() == 0:
            self._add_initial_nodes()
        else:
            # check if the previous node was 
            self._add_initial_nodes()
            self._find_root_edge(X_Y_R)

