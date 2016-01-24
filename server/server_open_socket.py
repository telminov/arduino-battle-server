# -*- coding: utf-8 -*-
import socket


#порт выбираем с от 1024-65535
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1) #кол-во слушателей

conn, addr = sock.accept() #принимаем подключение

print 'connected:', addr

#получаем данные
while True:
    data = conn.recv(1024) #кол-во байт для чтения
    if not data:
        break
    conn.send(data.upper())

#Закрытие соединения
conn.close()