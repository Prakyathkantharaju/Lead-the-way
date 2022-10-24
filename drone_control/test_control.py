from djitellopy import Tello

tello = Tello(retry_count=10)

tello.connect()

tello.takeoff()

# tello.move_left(100)

tello.rotate_counter_clockwise(90)

tello.land()