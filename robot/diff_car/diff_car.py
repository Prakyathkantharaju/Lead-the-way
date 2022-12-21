
# This code will be run on the rpi (inside your car).
# This will be the main file that you will run to control your car movement.


# Import the libraries that we need to use
import numpy as np
from AlphaBot import AlphaBot
from UDPComms import Subscriber, Publisher, timeout, Scope
import pickle
import zmq
import time
import cv2




# Create a class for the robot
class diff_car:
    def __init__(self, name: str, config: dict):
        # Call the base class constructor
        self.sub = Subscriber(port = 8889 )
        self.name = name
        self.config = config
        self.ab = AlphaBot()
        self.speed = self.config["speed"]
        self.pub_port = self.config["pub_port"]
        self.pub_ip = self.config["pub_ip"]
        self.pub_topic = self.config["pub_topic"]
        self.location = 0
        self.camera = cv2.VideoCapture(0) #type: ignore
        self.npimage = np.empty((480, 640, 3), dtype=np.uint8)
        self._initialize_speed()
        self.COMMAND_RATE  = 0.1
        self._last_control = time.time()

    def _initialize_speed(self):
        self.ab.setPWMA(self.speed)
        self.ab.setPWMB(self.speed)

    def _update_distance(self, update_rotation: np.ndarray):
        return self.location + update_rotation

    def Update(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        ip_port = "tcp://{}:{}".format(self.pub_ip, self.pub_port)
        print(ip_port)
        socket.bind(ip_port)
        time.sleep(2)
        while True:
            try: #type: ignore
                data = self.sub.get()


                _ = self._control(data['command'], data['speed'])
                time.sleep(self.COMMAND_RATE) # motor is running
                self.speed = 0 # stop
                self._initialize_speed()
                # self._last_control = time.time()
                    
                success, frame = self.camera.read()
                if success:
                    
                    self.npimage = np.array(frame)

                    dict = {'location': self.location, 'img': self.npimage,
                            'command': data['command'], 'speed': data['speed'],
                            'time':time.time() - self._last_control
                            }
                    data = pickle.dumps(dict)
                    socket.send_string(self.pub_topic, flags=zmq.SNDMORE)
                    socket.send_pyobj(data)
                    print(f"Sent data to {self.pub_topic}")
                    

                else:
                    print("Error reading frame")
                    
            except timeout: #type: ignore
                pass #type: ignore

    def _control(self, direction: str, speed: int = 40):
        Rotation_A = np.array([0, 0, 0])
        print(direction, speed)
        if speed != self.speed:
            print("updating speed to", speed)
            
            self.speed = speed
            self._initialize_speed()

        if direction == "forward":
            self.ab.forward()
            Rotation_A[0] = 1

        elif direction == "backward":
            self.ab.backward()
            Rotation_A[0] = -1

        elif direction == "left":
            self.ab.left()
            Rotation_A[1] = 1

        elif direction == "right":
            self.ab.right()
            Rotation_A[1] = -1

        elif direction == "stop":
            self.ab.stop()
        else:
            print("Invalid direction")
        self._update_distance(Rotation_A)

        return self.location

if __name__ == "__main__":
    # Create a robot object
    robot = diff_car("diff_car", {"speed": 0,
                                  "pub_port": 5557, "pub_ip": "0.0.0.0",
                                  "pub_topic": "diff_car"})
    robot.Update()
