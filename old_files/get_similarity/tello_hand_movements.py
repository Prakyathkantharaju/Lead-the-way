from djitellopy import Tello
import cv2, time
from human_direction import HumanMovementCommand
from Graph import Graph_structure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import skvideo.io
from tqdm import tqdm

G = Graph_structure()
hmc = HumanMovementCommand()

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
for i in tqdm(range(100)):
    hmc.get_command()
    frame = frame_read.frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if i % 15 == 0:
        G.add_images(frame, [1,0,0])
        nx.draw(G.Graph, ax=ax, with_labels=True)
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    data = cv2.resize(data, (480, 852), interpolation=cv2.INTER_AREA)

    frame = cv2.resize(frame, (480, 852), interpolation=cv2.INTER_AREA)

    frame_1 = np.concatenate((frame, data), axis = 1)
    
    if hmc.START:

        if not Takeoff:
            tello.takeoff()
            Takeoff = True

        if hmc.STOP:
            tello.land()
            hmc.START = False
            Takeoff = False


        if hmc.forward > 0:
            tello.move_forward(hmc.forward * 50)

        if hmc.Rotate > 0:
            tello.rotate_clockwise(np.rad2deg(hmc.Clock_wise))
        
        if hmc.Rotate < 0:
            tello.rotate_counter_clockwise(np.rad2deg(hmc.Anti_Clock_wise))

        if hmc.sideways > 0:
            tello.move_forward(hmc.forward * 20)

    # if i == 0:
    #     video_data = frame_1[np.newaxis, :]
    # else:
    #     video_data = np.concatenate((video_data, frame_1[np.newaxis,:]), axis=0)
    video_data.append(frame_1)
    
    time.sleep(1/30)


skvideo.io.vwrite("test_live_video.mp4", np.array(video_data))
nx.draw(G.Graph)
plt.show()
    
# keepRecording = False





