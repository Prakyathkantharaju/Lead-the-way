from matplotlib import ArrayLike
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

from typing import Tuple

import warnings
warnings.filterwarnings("ignore")


class Graph_data(object):

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
        return (img[:,dim // 3, :], img[:, dim//3 :dim*2//3, :], img[:,-dim//3:, :])

    def _get_features(self, image: npt.ArrayLike) -> None:
        img = Image.fromarray(image)
        img_transformed = self.tranformation(img).unsqueeze(0).to("cuda")
        im_vec = torch.tensor(self.model.extract_features(img_transformed).view(-1)).unsqueeze(0)
        return im_vec
 
    def add_images(self, img: npt.ArrayLike) -> float:
        self.images = self._get_three_images(img)

    def _add_node(self, number: int, features: npt.ArrayLike) -> None:
        self.Graph.add_node(number, features = features)

    def _add_initial_nodes(self):
        self.features = []
        central_nodes = 0
        number = self.Graph.number_of_nodes()
        nodes_add = []
        for i in range(3):
            self.features.append(self._get_features(self.images[i]))
            self._add_node(number + i, self.features[-1])
        

    def _process_images(self) -> None:
        if self.Graph.number_of_nodes() == 0:
            self._add_initial_nodes()
