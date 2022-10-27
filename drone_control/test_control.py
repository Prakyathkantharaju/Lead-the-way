from djitellopy import Tello
from human_direction_simple import HumanMovementCommand
import numpy as np


tello = Tello(retry_count=10)
hmc = HumanMovementCommand()

tello.connect()

tello.takeoff()

Takeoff = True

while Takeoff:

    hmc.get_command()

    if hmc.STOP:
        tello.land()
        hmc.START = False
        Takeoff = False


    if hmc.forward > 0:
        print("forward")
        tello.move_forward(100)

    if hmc.Rotate > 0:
        print("Rot")
        tello.rotate_clockwise(10)
    
    if hmc.Rotate < 0:
        print("Anti Rot")
        tello.rotate_counter_clockwise(10)

    if hmc.sideways > 0:
        tello.move_forward(80)


tello.land()