from UDPComms import Publisher, Scope
from time import sleep
import dataclasses
import pygame

# load the parent
from control import Control #type: ignore

@dataclasses.dataclass
class command:
    left: str = "left"
    right: str = "right"
    forward: str = "forward"
    backward: str = "backward"
    stop: str = "stop"

class Diff_controller(Control):
    def __init__(self, ip: str, port: int):
        super().__init__()
        self.pub = Publisher(port=port, scope=Scope.NETWORK)
        # self.pub.BROADCAST_IP = ip # type: ignore
        self.dict_send = {}
        self.dict_send["speed"] = 40
        self.dict_send["command"] = "forward"
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
                    self.dict_send["command"] = command.forward
                elif key[pygame.K_DOWN]:
                    self.dict_send["command"] = command.backward
                elif key[pygame.K_LEFT]:
                    self.dict_send["command"] = command.left
                elif key[pygame.K_RIGHT]:
                    self.dict_send["command"] = command.right
                elif key[pygame.K_SPACE]:
                    self.dict_send["command"] = command.stop        
                else:
                    continue

            
                print(self.dict_send)
                self.pub.send(self.dict_send)
                sleep(0.5)
                pygame.display.flip()
                pygame.time.wait(100)


if __name__ == "__main__":
    control = Diff_controller("192.168.0.115", 5557)
    control.update()




        
