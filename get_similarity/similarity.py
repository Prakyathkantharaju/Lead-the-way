from djitellopy import Tello
import cv2, time
from Graph import Graph_structure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
# import skvideo.io
from tqdm import tqdm
import pygame.camera
import pygame.image
import sys


# CODE to testout graph generation no information movement will be programmed.

###############################
###### COMMON FLAG ###########

SHOW_WINDOW = True
START_GRAPH = False












# G = Graph_structure()

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()
Takeoff = False


height, width, _ = frame_read.frame.shape
video_data = []
video_data_storage = []

fig, ax = plt.subplots(1,1)
data = np.zeros((height, width,3), dtype=np.uint8)

# start graph
Graph = Graph_structure()

if SHOW_WINDOW:
    screen =  pygame.display.set_mode( ( width * 2, height ) )
    pygame.display.set_caption("pygame drone view")

i = 0
while True:
    i += 1
    img = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
    # print(i, img.shape)


    if SHOW_WINDOW:

        for e in pygame.event.get():
            # print(e.type, pygame.K_s)

            if e.type == pygame.QUIT:
                sys.exit()

        
        if not pygame.key.get_focused():
            pass
        else:
            key = pygame.key.get_pressed()
            if key[pygame.K_s] == 1:
                print(f"Start data collection")
                # started graphing
                START_GRAPH = True
        

        if START_GRAPH and i%30 == 0:
            Graph.add_images(img, [1,0,0])
            nx.draw(Graph.Graph, ax = ax, with_labels = True)
            fig.canvas.draw()
            # Now we can save it to a numpy array.  
            data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # else:
            # data = img
        data = cv2.resize(data, (width, height), interpolation=cv2.INTER_AREA)

        img = np.concatenate((data, img), axis = 1)

    time.sleep(0.5)
                        


        



    pygame_img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")


    screen.blit(pygame_img, (0,0))
    pygame.display.flip()






