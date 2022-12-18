
# This code will be run on the rpi (inside your car).
# This will be the main file that you will run to control your car movement.


# Import the libraries that we need to use
import numpy as np
from AlphaBot import AlphaBot
from UDPComms import Subscriber, Publisher, timeout, Scope



# Create a class for the robot
class diff_car:
    def __init__(self, name: str, config: dict):
        # Call the base class constructor
        self.sub = Subscriber(port = 8888)
        self.name = name
        self.config = config
        self.ab = AlphaBot()
        self.speed = self.config["speed"]
        self.location = 0
        self._initialize_speed()

    def _initialize_speed(self):
        self.ab.setPWMA(self.speed)
        self.ab.setPWMB(self.speed)

    def _update_distance(self, update_rotation: np.ndarray):
        return self.location + update_rotation

    def Update(self):
        while True:
            try: #type: ignore
                data = self.sub.get()
                output = self._control(data['command'], data['speed'])
            expect timeout: #type: ignore
                pass #type: ignore

    def _control(self, direction: str, speed: int = 40):
        Rotation_A = np.array([0, 0, 0])
        if speed != self.speed:
            self.speed = speed

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
    robot = diff_car("diff_car", {"speed": 40, "return_ip": "192.168.0.102"})
    robot.Update()
