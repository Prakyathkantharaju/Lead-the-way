from bottle import get,post,run,route,request,template,static_file
import threading
import socket #ip
from Drone import DroneControl
from Diff_control import DiffControl
Drone = DroneControl(8888)
Diff = DiffControl(8889)

# car = AlphaBot()
class main(object):
    def __init__(self) -> None:
        # control
        # self.drone = DroneControl(8888)
        # self.diff_control = DiffControl(8889)
        pass



    @get("/")
    def index():
        return template("index")
        
    @route('/<filename>')
    def server_static(filename):
        return static_file(filename, root='./')

    @route('/fonts/<filename>')
    def server_fonts(filename):
        return static_file(filename, root='./fonts/')
	
    @post("/cmd")
    def cmd():
        global Drone
        global Diff
        code = request.body.read().decode()
        speed = request.POST.get('speed')
        if(speed != None):
            print(speed)

        if 'alphabot' in code:
            Drone.update(code)

        if 'Drone' in code:
            Diff.update(code)


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
localhost=s.getsockname()[0]
run(host = localhost, port = 8000)
