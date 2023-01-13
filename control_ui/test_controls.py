from UDPComms import Subscriber, Scope, timeout
import time


def subscriber_test(port: int):
    sub = Subscriber(port=port, scope=Scope.NETWORK)
    while True:
        try:
            data = sub.get()
            print(data)
        except timeout:
            pass
        time.sleep(0.5)


if __name__ == "__main__":
    subscriber_test(8889)   