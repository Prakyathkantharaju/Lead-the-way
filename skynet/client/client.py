
"""Example using zmq with asyncio with pub/sub and dealer/router for asynchronous messages

Publisher sends either 'Hello World' or 'Hello Sekai' based on class language setting,
which is received by the Subscriber

When the Router receives a message from the Dealer, it changes the language setting"""

# Copyright (c) Stef van der Struijk.
# This example is in the public domain (CC-0)

import asyncio
import logging
import traceback

import zmq
import zmq.asyncio
from zmq.asyncio import Context
import pickle


# data storeing classes for each robot
from diff_car import DiffCar
from drone import Drone



# manages message flow between publishers and subscribers
class MainReceiver:
    def __init__(self, url: str = '127.0.0.1', port: int = 5555):
        # get ZeroMQ version
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.__version__)

        self.url = f"tcp://{url}:{port}"
        # pub/sub and dealer/router
        self.ctx = Context.instance()

        # init hello world publisher obj
        self.diff_car_config = DiffCar()

        self.drone_config = Drone()

    def main(self) -> None:

        # activate publishers / subscribers
        asyncio.run(
            asyncio.wait(
                [
                    self.quad(),
                    self.drone(),
                    self.diff_car()
                ]
            )
        )

    # processes message topic 'world'; "Hello World" or "Hello Sekai"
    async def drone(self) -> None:
        print("Setting up world sub")
        # setup subscriber
        sub = self.ctx.socket(zmq.SUB)
        url = f"tcp://{'127.0.0.1'}:{5556}"
        sub.connect(url)
        sub.setsockopt(zmq.SUBSCRIBE, b'drone')
        print("World sub initialized")

        # without try statement, no error output
        try:
            # keep listening to all published message on topic 'world'
            while True:
                topic = await sub.recv_string()
                msg = await sub.recv_pyobj()
                print(f"world sub; topic: {topic}\tmessage: {pickle.loads(msg)}")
                self.drone_config.processing_function(msg)
                # process message

                await asyncio.sleep(1)

                # publish message to topic 'sekai'
                # async always needs `send_multipart()`
                # await pub.send_multipart([b'sekai', msg_publish.encode('ascii')])

        except Exception as e:
            print("Error with sub world")
            # print(e)
            logging.error(traceback.format_exc())
            print()

        finally:
            # TODO disconnect pub/sub
            pass
    # processes message topic 'world'; "Hello World" or "Hello Sekai"
    async def diff_car(self) -> None:
        print("Setting up world sub")
        # setup subscriber
        sub = self.ctx.socket(zmq.SUB)
        url = f"tcp://{'127.0.0.1'}:{5557}"
        sub.connect(url)
        sub.setsockopt(zmq.SUBSCRIBE, b'diff_car')
        print("World sub initialized")

        # without try statement, no error output
        try:
            # keep listening to all published message on topic 'world'
            while True:
                topic = await sub.recv_string()
                msg = await sub.recv_pyobj()

                # process message
                self.diff_car_config.process_function(msg)


                await asyncio.sleep(1)

                # publish message to topic 'sekai'
                # async always needs `send_multipart()`
                # await pub.send_multipart([b'sekai', msg_publish.encode('ascii')])

        except Exception as e:
            print("Error with sub world")
            # print(e)
            logging.error(traceback.format_exc())
            print()

        finally:
            # TODO disconnect pub/sub
            pass

    # processes message topic 'world'; "Hello World" or "Hello Sekai"
    async def quad(self) -> None:
        print("Setting up world sub")
        # setup subscriber
        sub = self.ctx.socket(zmq.SUB)
        sub.connect(self.url)
        sub.setsockopt(zmq.SUBSCRIBE, b'quad')
        print("World sub initialized")

        # without try statement, no error output
        try:
            # keep listening to all published message on topic 'world'
            while True:
                topic = await sub.recv_string()
                msg = await sub.recv_pyobj()
                print(f"world sub; topic: {topic}\tmessage: {pickle.loads(msg)}")
                # process message

                await asyncio.sleep(1)

                # publish message to topic 'sekai'
                # async always needs `send_multipart()`
                # await pub.send_multipart([b'sekai', msg_publish.encode('ascii')])

        except Exception as e:
            print("Error with sub world")
            # print(e)
            logging.error(traceback.format_exc())
            print()

        finally:
            # TODO disconnect pub/sub
            pass



def main() -> None:
    hello_world = MainReceiver()
    hello_world.main()


if __name__ == '__main__':
    main()

