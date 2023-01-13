from UDPComms import Publisher, Scope
import time
import dataclasses

# load the parent
from control import Control #type: ignore

@dataclasses.dataclass
class Diffcommand:
    left: str = "left"
    right: str = "right"
    forward: str = "forward"
    backward: str = "backward"
    stop: str = "stop"

class DiffControl(Control):
    def __init__(self, port: int):
        super().__init__()
        self.pub = Publisher(port=port, scope=Scope.NETWORK)
        # self.pub.BROADCAST_IP = ip # type: ignore
        self.dict_send = {}
        self.dict_send["speed"] = 40
        self.dict_send["command"] = "forward"

    def update(self, command: str):
        print(command)

        if command == "alphabot-forward":
            self.dict_send["command"] = Diffcommand.forward
        elif command == "alphabot-backward":
            self.dict_send["command"] = Diffcommand.backward
        elif command == "alphabot-turnleft":
            self.dict_send["command"] = Diffcommand.left
        elif command == "alphabot-turnright":
            self.dict_send["command"] = Diffcommand.right
        elif command == "alphabot-stop":
            self.dict_send["command"] = Diffcommand.stop
        else:
            pass
        self.pub.send(self.dict_send)
        time.sleep(0.5)


if __name__ == "__main__":
    control = Diff_controller(8889)
    control.update()




        
