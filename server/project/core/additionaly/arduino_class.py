# -*-coding:utf8 -*-
import serial
import os
import sys
import time

#port = '/dev/ttyACM0'
class Arduino():
    def __init__(self, usb_port, speed_connected=9600, dsrdtr=1, timeout=0):
        self.usb_port = usb_port
        self.ser = serial.Serial(usb_port, speed_connected, dsrdtr = dsrdtr,timeout = timeout)

    def send(self, data):
        self.ser.write(data)

    def get(self):
        data = self.ser.readline().split('\r\n')[0]
        print data
        return data

    def close_connect(self):
        self.ser.close()