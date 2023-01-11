#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
# from AlphaBot import AlphaBot
import threading
import socket #ip
import os,sys

# car = AlphaBot()

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
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    # print(code)
    # print(speed)
    if(speed != None):
        # car.setPWMA(float(speed))
        # car.setPWMB(float(speed))
        print(speed)
    if code == "stop":
        pass
        # car.stop()
        # print("stop")
    elif code == "alphabot-forward":
        # car.forward()
        print("alphabot-forward")
    elif code == "alphabot-backward":
        # car.backward()
        print("alphabot-backward")
    elif code == "alphabot-turnleft":
        # car.left()
        print("alphabot-turnleft")
    elif code == "alphabot-turnright":
        # car.right()
        print("alphabot-turnright")
    elif code == "Drone-forward":
        # car.forward()
        print("Drone-forward")
    elif code == "Drone-backward":
        # car.backward()
        print("Drone-backward")
    elif code == "Drone-turnleft":
        # car.left()
        print("Drone-turnleft")
    elif code == "Drone-turnright":
        # car.right()
        print("Drone-turnright")
    elif code == "Drone-up":
        # car.forward()
        print("Drone-up")
    elif code == "Drone-rotation-clock":
        # car.backward()
        print("Drone-rotation-clock")
    elif code == "Drone-rotation-anti-clock":
        # car.left()
        print("Drone-rotation-anti-clock")
    elif code == "Drone-down":
        # car.right()
        print("Drone-down")
    else:
        value = 0
        # try:
            # value = int(speed)
            # if(value >= 0 and value <= 100):
                # print(value)
                # car.setPWMA(value)
                # car.setPWMB(value)
        # except:
            # print("Command error")
    return "OK"

# def camera():
#     lastpath = os.path.abspath(os.path.join(os.getcwd(), "../"))
#     print("lastpath = %s" %lastpath)
#     campath = lastpath + '/mjpg-streamer/mjpg-streamer-experimental/'
#     print("campath = %s" %campath)
#     os.system(campath  + './mjpg_streamer -i "' + campath + './input_uvc.so" -o "' + campath + './output_http.so -w ' + campath + './www"') 

# tcamera = threading.Thread(target = camera)
# tcamera.setDaemon(True)
# tcamera.start()

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
localhost=s.getsockname()[0]
run(host = localhost, port = 8000)
