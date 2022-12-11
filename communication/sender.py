from time import sleep
import zmq
import pickle

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
sleep(2)

i=0
topic = 'quad'
while True:
    i += 1
    frame = pickle.dumps([i])
    socket.send_string(topic, zmq.SNDMORE)
    socket.send_pyobj(frame)
    print('Sent frame {}'.format(i))
    sleep(1)
    print(i)

