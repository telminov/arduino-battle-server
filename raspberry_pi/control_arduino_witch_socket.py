# -*-coding:utf8 -*-
from arduino_class import Arduino
from client_socket_class import SocketClient

#подключение к ардуино
usb_port = '/dev/ttyACM0' 
arduino = Arduino(usb_port=usb_port)

#подключение к вещательному сокету
socket = SocketClient('10.0.0.6', 9090)

while True:
	if socket.get_data(1024):
		print socket.get_data(1024)
		arduino.send(socket.get_data(1024))