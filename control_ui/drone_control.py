from control import Control
import pygame
import dataclasses
import time
from UDPComms import Publisher, Scope, timeout



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
    HOVER: str = "hover" # else case
    CW: str = "cw"
    CCW: str = "ccw"



class Drone_controller(Control):
    def __init__(self, port: int):
        super().__init__()
        self.pub = Publisher(port=port, scope=Scope.NETWORK)
        # self.pub.BROADCAST_IP = ip # type: ignore
        self.dict_send = {}
        self.dict_send["speed"] = 20
        self.dict_send["command"] = command.HOVER
        pygame.init()
        self.screen = pygame.display.set_mode((500, 250))
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = self.myfont.render('Hello World! click to enable', 
                                         False, (220, 0, 0))

        self.screen.fill((255, 255, 255))
        self.screen.blit(textsurface,(40,100))

    def update(self):
        while True:
            pygame.event.pump()

            if pygame.key.get_focused():
                key = pygame.key.get_pressed()
                if key[pygame.K_UP]:
                    self.dict_send["command"] = command.FORWARD
                elif key[pygame.K_DOWN]:
                    self.dict_send["command"] = command.BACKWARD
                elif key[pygame.K_LEFT]:
                    self.dict_send["command"] = command.CCW
                elif key[pygame.K_RIGHT]:
                    self.dict_send["command"] = command.CW
                elif key[pygame.K_SPACE]:
                    self.dict_send["command"] = command.HOVER
                elif key[pygame.K_w]:
                    self.dict_send["command"] = command.UP
                elif key[pygame.K_s]:
                    self.dict_send["command"] = command.DOWN
                elif key[pygame.K_q]:
                    self.dict_send["command"] = command.TAKEOFF
                elif key[pygame.K_e]:
                    self.dict_send["command"] = command.LAND
                elif key[pygame.K_a]:
                    self.dict_send["command"] = command.LEFT
                elif key[pygame.K_d]:
                    self.dict_send["command"] = command.RIGHT
                elif key[pygame.K_f]:
                    self.dict_send["speed"] += 1
                else:
                    continue

            
                print(self.dict_send)
                self.pub.send(self.dict_send)
                time.sleep(0.5)
                pygame.display.flip()
                pygame.time.wait(100)


if __name__ == "__main__":
    control = Drone_controller(8888)
    control.update()

