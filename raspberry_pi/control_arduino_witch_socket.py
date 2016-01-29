# -*-coding:utf8 -*-
from arduino_class import Arduino
from client_socket_class import SocketClient
import time

#подключение к ардуино
usb_port = '/dev/ttyACM0' 
arduino = Arduino(usb_port=usb_port)

#подключение к вещательному сокету
socket = SocketClient('10.0.0.6', 9090)

while True:
	time.sleep(2)
	print 1
	from_arduino_data = arduino.get()
	if from_arduino_data:
		print from_arduino_data
		socket.send(from_arduino_data)
		print 2

	# print 3
	# if socket.get():
	# 	print 4
	# 	socket_get = socket.get(1024)
	# 	print socket_get
	# 	arduino.send(socket_get)

