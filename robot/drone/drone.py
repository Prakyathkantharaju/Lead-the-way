from ..robot import robot
from djitellopy import Tello
import numpy as np
import time
import dataclasses
from UDPComms import Subscriber, Scope, timeout
import zmq
import pickle
from typing import List

@dataclasses.dataclass
class command:
    LEFT: str = "left"
    RIGHT: str = "right"
    FORWARD: str = "forward"
    BACKWARD: str = "backward"
    STOP: str = "stop"
    TAKEOFF: str = "takeoff"
    LAND: str = "land"
    UP: str = "up"
    DOWN: str = "down"

class Drone(robot):
    def __init__(self, config: dict) -> None:
        super().__init__(name=config['name'],config=config) # Call the parent class constructor
        self._name = config['name']
        self.speed = config['speed']
        self.tello = Tello()
        self.subscriber = Subscriber(port = config['sub_port'], scope = Scope.NETWORK)

        # skynet client connection
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        ip = config['serv_ip']
        port = config['serv_port']
        self.socket.bind(f"tcp://{ip}:{port}")
        self.pub_topic = config['pub_topic']
        self.start_time = time.time()
        self.state = [0, 0, 0]



        # default controller 
        self.left_right_velocity = 0
        self.for_back_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0




    def control(self) -> None:
        print("Drone is running")
        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()
        frame_read = self.tello.get_frame_read()
        while True:
            try:
                data = self.subscriber.get()
                self._update_constants(data['command'], data['speed'])
                self._update_drone()
                img = frame_read.frame
                self._package_send(img)
                time.sleep(1 / 30)
                if frame_read.stopped:
                    break
            except timeout:
                pass
        self.tello.end()

    def _package_send(self, img: np.ndarray) -> None:
        self.state = [self.for_back_velocity, 
                    self.left_right_velocity, 
                    self.up_down_velocity]
        time = time.time() - self.start_time #type: ignore
        self.socket.send_string(self.pub_topic, zmq.SNDMORE)
        dict_store = {'location': self.state, 'time': time, 'img': img}
        data = pickle.dumps(dict_store)
        self.socket.send_pyobj(data)
        print(f"sent data to {self.pub_topic}")
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0


    def _update_constants(self, cmd: str, speed: int) -> None:
        if cmd == command.TAKEOFF:
            self.tello.takeoff()
        elif cmd == 'land':
            self.tello.land()
        elif cmd == 'forward':
            self.for_back_velocity += speed
        elif cmd == 'backward':
            self.for_back_velocity -= speed
        elif cmd == 'up':
            self.up_down_velocity += speed
        elif cmd == 'down':
            self.up_down_velocity -= speed
        elif cmd == 'cw':
            self.left_right_velocity += speed
        elif cmd == 'ccw':
            self.left_right_velocity += speed
        else:
            print('Command not recognized...')


    def _update_drone(self) -> None:
        self.tello.send_rc_control(self.left_right_velocity, 
                                   self.for_back_velocity,
                                   self.up_down_velocity, 
                                   self.yaw_velocity)
    def get_config(self) -> dict:
        return self.config

    def get_state(self) -> List[int]:
        return self.state
        # frame = frame_read.frame
        # # battery n. 电池
        # text = "Battery: {}%".format(self.tello.get_battery())
        # cv2.putText(frame, text, (5, 720 - 5),
        #     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 
        # frame = np.rot90(frame)
        # frame = np.flipud(frame)



        # Call it always before finishing. To deallocate resources.






if __name__ == '__main__':
    config = {'name': 'drone',
              'speed': 60,
              'sub_port': 8888,
              'serv_ip': '127.0.0.1',
              'serv_port': 5556,
              }

    drone = Drone(config)
    drone.control()
    
