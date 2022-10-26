import cv2
import pygame
import numpy as np
import time

class HumanMovementCommand:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.win = pygame.display.set_mode((500,250))
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render("Click to enable", False, ( 220, 0, 0))
        self.win.fill((255, 255, 255))
        # self.win.bilt(text_surface, (40, 100))

        # commands
        self.X_c  = 0
        self.Y_c = 0
        self.R_c = 0

        # persistent commands
        self.forward = 0
        self.sideways = 0
        self.Rotate = 0


    def get_command(self):
        pygame.event.pump()

        if not pygame.key.get_focused():
            pass
        else:
            key = pygame.key.get_pressed()
            if key[pygame.K_w] == 1:
                self.X_c += 1
            if key[pygame.K_a] == 1:
                self.Y_c += 1
            if key[pygame.K_s] == 1:
                self.X_c -= 1

            if key[pygame.K_d] == 1:
                self.Y_c -= 1

            if key[pygame.K_q] == 1:
                self.R_c += 0.1

            if key[pygame.K_e] == 1:
                self.R_c -= 0.1
        self._calculate_position()


    def _calculate_position(self):
        self.forward = self.X_c
        self.sideways = self.Y_c * np.cos(self.R_c) + self.X_c * np.sin(self.R_c)
        if self.R_c > 0:
            self.Clock_wise = np.rad2deg(self.R_c)
            self.Anti_Clock_wise = 0
            self.Rotate = self.R_c
        else:
            self.Anti_Clock_wise = np.rad2deg(self.R_c)
            self.Clock_wise = 0
            self.Rotate = self.R_c
        self.X_c = 0
        self.Y_c = 0
        self.R_c = 0
        print(self.forward, self.sideways, self.Anti_Clock_wise, self.Clock_wise)


if __name__ == "__main__":
    HMC = HumanMovementCommand()
    while True:
        print("here")
        HMC.get_command()
        pygame.display.flip()
        pygame.time.wait(int(1000/20))
        time.sleep(1)
