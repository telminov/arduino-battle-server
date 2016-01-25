# -*- coding:utf-8 -*-
import socket


class SocketClient():
    sock = socket.socket()

    def __init__(self, ip, port):
        self.port = port # порт, который задали на сервере
        self.ip = ip #ip Сервера
        self.sock.connect((ip, port)) #коннектимся

    def get_data(self, bites=10000):
        data = self.sock.recv(bites)#кол-во байт для чтения
        return data

    def send_data(self, data):
        self.sock.send(data)

    def close_connect(self):
        self.conn.close()
