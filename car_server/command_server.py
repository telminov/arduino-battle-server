# coding: utf-8
import asyncio
import os
import serial
import json
import zmq
import consts
import os.path


class ServerSettings:
    def __init__(self):
        self.address = None
        self.load()

    def set_address(self, address):
        with open(consts.SERVER_SETTINGS_PATH, 'w') as f:
            json.dump({'address': address}, f)
        self.address = address

    def load(self):
        if os.path.exists(consts.SERVER_SETTINGS_PATH):
            with open(consts.SERVER_SETTINGS_PATH) as f:
                self.address = json.load(f)['address']


class MovingState:
    def __init__(self):
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.speed = 0


class Command:
    def __init__(self, move_state: MovingState):
        self.move_state = move_state
        self.blink = False

    def get_arduino_repr(self) -> str:
        mask = '%i%i%i%i%i%i\n' % (
            self.move_state.forward,
            self.move_state.backward,
            self.move_state.left,
            self.move_state.right,
            self.move_state.speed,
            self.blink,
        )
        return mask


class CommandTransmitter:
    def __init__(self, moving_state: MovingState):
        self.moving_state = moving_state
        self.serial_arduino = None

    def connect_to_arduino(self):
        self.serial_arduino = serial.Serial(self._get_arduino_dev(), 9600, dsrdtr=1, timeout=0)
        self.serial_arduino.isOpen()

    def close(self):
        if self.serial_arduino.isOpen():
            self.serial_arduino.close()

    def blink(self):
        command = Command(move_state=self.moving_state)
        command.blink = True
        self._transmit_command(command)

    def _transmit_command(self, command: Command):
        arduino_repr = command.get_arduino_repr()
        self.serial_arduino.write(arduino_repr.encode())


    @staticmethod
    def _get_arduino_dev():
        for name in os.listdir('/dev'):
            if name.startswith('ttyACM'):
                return '/dev/%s' % name
        raise Exception('No Arduino devices detected')


class ServerHeartListener:
    def __init__(self, server: ServerSettings, transmitter: CommandTransmitter):
        self.transmitter = transmitter
        self.is_stopped = False
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        connect_address = 'tcp://%s:%s' % (server.address, consts.HEART_BEAT_PORT)
        print(connect_address)
        self.socket.connect(connect_address)
        self.socket.setsockopt(zmq.SUBSCRIBE, ''.encode())

    async def listen(self):
        while not self.is_stopped:
            try:
                data = self.socket.recv_json(flags=zmq.NOBLOCK)
                print('Server heart beat', data)
                self.transmitter.blink()
            except zmq.Again:
                await asyncio.sleep(0.1)

    def stop(self):
        self.is_stopped = True

    def close(self):
        self.socket.close()
        self.context.term()


class Car:

    def __init__(self):
        self.server_setting = ServerSettings()
        self.moving_state = MovingState()
        self.command_transmitter = CommandTransmitter(self.moving_state)
        # self.heart_listener = ServerHeartListener(self.server_setting.address)  # TODO case of initing in process of working

    def start(self):
        self.command_transmitter.connect_to_arduino()

async def wait_second():
    await asyncio.sleep(0.5)


if __name__ == '__main__':
    car = Car()
    car.start()

    heart_listener = ServerHeartListener(car.server_setting, car.command_transmitter)

    loop = asyncio.get_event_loop()
    heart_listener_task = loop.create_task(heart_listener.listen())

    tasks = asyncio.gather(
        heart_listener.listen()
    )

    try:
        loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        tasks.cancel()
        loop.run_forever()
        tasks.exception()
    finally:
        heart_listener_task.close()
        loop.close()


#
#
# class CommandTransmitter:
#     def start_listener_server(self):
#         print('Starting command listener server %s...' % self._get_server_address())
#         self.listener_context = zmq.Context()
#         self.listener_socket = self.listener_context.socket(zmq.PULL)
#         self.listener_socket.bind(self._get_server_address())
#         print('Command listener server start successfully!')
#
#     def connect_to_arduino(self):
#         self.serial_arduino = serial.Serial(self._get_arduino_dev(), 9600, dsrdtr=1, timeout=0)
#         self.serial_arduino.isOpen()
#
#     def listen(self):
#         # TODO: add stoping logic for case of lose signal
#         while True:
#             command_msg = self._get_latest_command()
#             print('Get command %s' % command_msg, datetime.datetime.now())
#
#             command_data = json.loads(command_msg)
#             command = self._message_to_command(command_data)
#             self._transmit_command(command)
#
#             # command_data['processed'] = True
#             # response = json.dumps(command_data)
#             # self.listener_socket.send_string(response)
#
#     def close(self):
#         if hasattr(self, 'listener_socket'):
#             self.listener_socket.close()
#             self.listener_context.term()
#         if hasattr(self, 'serial_arduino'):
#             self.serial_arduino.close()
#
#     @staticmethod
#     def _get_server_address():
#         address = 'tcp://*:%s' % consts.CAR_COMMAND_SERVER_PORT
#         return address
#
#     def _get_latest_command(self):
#         command = None
#         while True:
#             try:
#                 command = self.listener_socket.recv_string(flags=zmq.NOBLOCK)
#             except zmq.Again:
#                 if command is None:
#                     sleep(0.01)
#                 else:
#                     break
#         return command
#
#     @staticmethod
#     def _get_arduino_dev():
#         for name in os.listdir('/dev'):
#             if name.startswith('ttyACM'):
#                 return '/dev/%s' % name
#         raise Exception('No Arduino devices detected')
#
#     @staticmethod
#     def _message_to_command(command_data: dict) -> Command:
#         command = Command()
#         command.forward = command_data['forward']
#         command.backward = command_data['backward']
#         command.left = command_data['left']
#         command.right = command_data['right']
#         return command
#
#     def _transmit_command(self, command: Command):
#         arduino_repr = command.get_arduino_repr()
#         self.serial_arduino.write(arduino_repr.encode())
#
#
# if __name__ == '__main__':
#     transmitter = CommandTransmitter()
#     try:
#         transmitter.start_listener_server()
#         transmitter.connect_to_arduino()
#         transmitter.listen()
#     finally:
#         transmitter.close()
#
