# -*- coding: utf-8 -*-
import socket

sock = socket.socket()
sock.connect(('localhost', 9090)) #метод connect, с помощью которого мы подключаемся к серверу
sock.send('hello, world!')

data = sock.recv(1024)
sock.close()

print data