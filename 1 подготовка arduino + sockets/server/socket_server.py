# -*- coding:utf-8 -*-
import socket


class SocketServer():
    sock = socket.socket()

    def __init__(self, port, ip='0.0.0.0'):
        self.port = port
        self.ip = ip
        self.sock.bind((ip, port)) #открываем сокет с таким то портом
        self.sock.listen(1) #кол-во слушателей

    def accept(self):
        #принимаем подключение, как только его примет пойдем дальше
        #внимание, как нажмете выполнять функцию, вы не сможете ни чего предпринять пока не подключитесь
        self.conn, self.addr = self.sock.accept()
        #conn - устройство, которое к нам приконектилось
        print 'connected:', self.addr


    def get_data(self, bites=10000):
        data = self.conn.recv(bites)#кол-во байт для чтения
        return data

    def send_data(self, data):
        print data
        self.conn.send(data)

    def close_conn(self):
        self.conn.close()
