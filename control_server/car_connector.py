# coding: utf-8
import zmq
import consts
from core import models


class Commander:

    def __init__(self, car: models.Car):
        self.car = car

    def send_command(self, command: str) -> str:
        socket = self._get_socket()
        socket.send_string(command)
        response = socket.recv_string()
        return response

    def close(self):
        if self._has_socket():
            self._socket.close()
            self._context.term()
            del self._socket
            del self._context

    def _get_socket(self):
        if not self._has_socket():
            self._context = zmq.Context()
            self._socket = self._context.socket(zmq.REQ)
            self._socket.connect(self._get_car_server_address())
        return self._socket

    def _has_socket(self):
        return hasattr(self, '_socket')

    def _get_car_server_address(self):
        address = 'tcp://%s:%s' % (self.car.address, consts.CAR_COMMAND_SERVER_PORT)
        return address
