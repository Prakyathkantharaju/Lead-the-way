from djitellopy import Tello
import cv2, time
from human_direction import HumanMovementCommand
from Graph import Graph_structure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
# import skvideo.io
from tqdm import tqdm

G = Graph_structure()

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()
Takeoff = False



fig, ax = plt.subplots(1,1)

height, width, _ = frame_read.frame.shape
nx.draw(G.Graph, ax=ax, with_labels=True)
video_data = []
video_data_storage = []

while True:
    img = frame_read.frame
    img  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    G.add_images(img, [1,0,0])
    
    plt.imshow(img)

    # key = cv2.waitKey(1) & 0xff
    # if key == 27: # ESC
        # break
    plt.pause(0.001)




# skvideo.io.vwrite("test_live_video.mp4", np.array(video_data))
# nx.draw(G.Graph)
# plt.show()
    
# keepRecording = False





