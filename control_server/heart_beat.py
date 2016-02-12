# coding: utf-8
import datetime
from time import sleep
import zmq
import consts


class Heart:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)

    def beat(self):
        beat_msg = {
            'dt': datetime.datetime.now().isoformat(),
        }
        self.socket.send_json(beat_msg)
        # print(beat_msg)

    def start(self):
        self.socket.bind('tcp://*:%s' % consts.HEART_BEAT_PORT)

        while True:
            self.beat()
            sleep(1)

    def close(self):
        self.socket.close()
        self.context.term()

