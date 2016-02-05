# coding: utf-8
import zmq
import consts

ping_server_address = 'tcp://*:%s' % consts.CAR_COMMAND_SERVER_PORT
print('Starting ping server %s...' % ping_server_address)
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind(ping_server_address)
print('Ping server start successfully!')

while True:
    msg = socket.recv_string()
    print("Get ping message: %s" % msg)


