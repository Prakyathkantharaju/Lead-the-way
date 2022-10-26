from djitellopy import Tello
import cv2, time
from human_direction import HumanMovementCommand
from Graph import Graph_structure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from threading import Thread

G = Graph_structure()
hmc = HumanMovementCommand()

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    fig, ax = plt.subplots(1,1)

    while keepRecording:
        ax.cla()
        frame = frame_read.frame
        G.add_images(frame, [hmc.forward, hmc.sideways, hmc.Rotate])
        nx.draw(G.Graph, ax = ax, with_labels = True)
        print(frame.shape)
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        data = cv2.resize(data, (480, 852), interpolation=cv2.INTER_AREA)

        frame = cv2.resize(frame, (480, 852), interpolation=cv2.INTER_AREA)

        frame_1 = np.concatenate((frame, data), axis = 1)
        video.write(frame_1)
        time.sleep(1/10)
        cv2.imshow('frame', frame_1)
      
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video.release()


grapher = Thread(target=videoRecorder)

grapher.start()

grapher.join()
for i in range(10):
    print(i)
    time.sleep(1)
keepRecording = False





