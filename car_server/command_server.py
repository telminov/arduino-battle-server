# coding: utf-8
import datetime

import serial
import json
import zmq
import consts
import settings


class Command:
    def __init__(self):
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

    def get_arduino_repr(self) -> str:
        mask = '%i%i%i%i\n' % (
            self.forward,
            self.backward,
            self.left,
            self.right,
        )
        return mask


class CommandTransmitter:
    def start_listener_server(self):
        print('Starting command listener server %s...' % self._get_server_address())
        self.listener_context = zmq.Context()
        self.listener_socket = self.listener_context.socket(zmq.REP)
        self.listener_socket.bind(self._get_server_address())
        print('Command listener server start successfully!')

    def connect_to_arduino(self):
        self.serial_arduino = serial.Serial(settings.ARDUINO_DEV, 9600, dsrdtr=1, timeout=0)
        self.serial_arduino.isOpen()


    def listen(self):
        # TODO: add stoping logic for case of lose signal
        while True:
            command_msg = self.listener_socket.recv_string()
            print('Get command %s' % command_msg, datetime.datetime.now())

            command_data = json.loads(command_msg)
            command = self._message_to_command(command_data)
            self._transmit_command(command)

            command_data['processed'] = True
            response = json.dumps(command_data)
            self.listener_socket.send_string(response)

    def close(self):
        if hasattr(self, 'listener_socket'):
            self.listener_socket.close()
            self.listener_context.term()
        if hasattr(self, 'serial_arduino'):
            self.serial_arduino.close()

    @staticmethod
    def _get_server_address():
        address = 'tcp://*:%s' % consts.CAR_COMMAND_SERVER_PORT
        return address

    def _message_to_command(self, command_data: dict) -> Command:
        command = Command()
        command.forward = command_data['forward']
        command.backward = command_data['backward']
        command.left = command_data['left']
        command.right = command_data['right']
        return command

    def _transmit_command(self, command: Command):
        arduino_repr = command.get_arduino_repr()
        self.serial_arduino.write(arduino_repr.encode())


if __name__ == '__main__':
    transmitter = CommandTransmitter()
    try:
        transmitter.start_listener_server()
        transmitter.connect_to_arduino()
        transmitter.listen()
    finally:
        transmitter.close()

