from control import Control
from UDPComms import Publisher, Scope
import dataclasses
import time



@dataclasses.dataclass
class Dronecommand:
    LEFT: str = "left"
    RIGHT: str = "right"
    FORWARD: str = "forward"
    BACKWARD: str = "backward"
    STOP: str = "stop"
    TAKEOFF: str = "takeoff"
    LAND: str = "land"
    UP: str = "up"
    DOWN: str = "down"
    HOVER: str = "hover" # else case
    CW: str = "cw"
    CCW: str = "ccw"


class DroneControl(Control):
    def __init__(self, port: int):
        super().__init__()
        self.pub = Publisher(port=port, scope=Scope.NETWORK)
        self.dict_send = {}
        self.dict_send["speed"] = 20
        self.dict_send["command"] = Dronecommand.HOVER

    def update(self, command: str):
        print(command)
        if command == "Drone-forward":
            self.dict_send["command"] = Dronecommand.FORWARD
        elif command == "Drone-backward":
            self.dict_send["command"] = Dronecommand.BACKWARD
        elif command == "Drone-left":
            self.dict_send["command"] = Dronecommand.LEFT
        elif command == "Drone-right":
            self.dict_send["command"] = Dronecommand.RIGHT
        elif command == "Drone-up":
            self.dict_send["command"] = Dronecommand.UP
        elif command == "Drone-down":
            self.dict_send["command"] = Dronecommand.DOWN
        elif command == "Drone-ccw": 
            self.dict_send["command"] = Dronecommand.CCW
        elif command == "Drone-cw":
            self.dict_send["command"] = Dronecommand.CW
        elif command == "Drone-takeoff":
            self.dict_send["command"] = Dronecommand.TAKEOFF
        elif command == "Drone-land":
            self.dict_send["command"] = Dronecommand.LAND
        elif command == "Drone-fast":
            self.dict_send["speed"] += 1
        elif command == "Drone-slow":
            self.dict_send["speed"] -= 1
        else:
            pass

        self.pub.send(self.dict_send)
        time.sleep(0.5)



        


