from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
from get_similarity.Graph_v2 import Graph_structure
import matplotlib.pyplot as plt
import networkx as nx

# Speed of the drone

S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.

FPS = 120


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.


    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Left Tello stream | Right knowledge graph")
        self.screen = pygame.display.set_mode([960 * 2, 720])

        # Init Tello object that interacts with the Tello drone
        # 初始化与Tello交互的Tello对象
        self.tello = Tello()

        # Drone velocities between -100~100
        # 无人机各方向速度在-100~100之间
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

        # Custom setting realted to graph creating
        self.COUNTER  = 0
        self.graph = Graph_structure()
        self.action_array = [0,0,0]
        self.fig, self.ax = plt.subplots(1,1)
        self.action_array = [0,0,0]
        self.data = np.ones((960, 720,3), dtype=np.uint8) *255
        self.save_counter = 0

    def _graph_helper(self, img):
        if self.graph.Graph.number_of_nodes() > 30:
            print("#######" * 100)
            print("storing the data")
        
            self.save_counter += 1
            nx.write_gpickle(self.graph.Graph, f"graph_store/graph_data_{self.save_counter}.gpickle")
            self.graph.Graph = nx.Graph()
            self.action_array = [0,0,0]

        self.ax.cla()
        self.graph.add_images(img, self.action_array)
        nx.draw(self.graph.Graph, ax = self.ax, with_labels = True)
        self.fig.canvas.draw()
        data = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        data = cv2.resize(data, (720, 960), interpolation=cv2.INTER_AREA)
        self.COUNTER = 0
        # self.action_array = [0, 0, 0]
        return data

        

    def run(self):

        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:
            self.COUNTER += 1

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n. 电池
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            if self.COUNTER == 10:
                self.data = self._graph_helper(frame)
            frame = np.concatenate((frame, self.data), axis = 0)


            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)



        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key

        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key

        
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello.

            
        """
        if self.send_rc_control:
            print(self.left_right_velocity, self.for_back_velocity, self.yaw_velocity, self.action_array)
            self.action_array[0] += self.left_right_velocity
            self.action_array[1] += self.for_back_velocity
            self.action_array[2] += self.yaw_velocity
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend

    frontend.run()


if __name__ == '__main__':
    main()
