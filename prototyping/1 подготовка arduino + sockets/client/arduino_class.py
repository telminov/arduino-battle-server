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
        print self.ser.readline()
        return self.ser.readline()

    def close_connect(self):
        self.ser.close()

    def printAnalogDat(self):
        while 1:
            #запуск чтения из порта и маршрутизация по файлам
            try:
                print self.mySerialDecode()

            #выход по Ctrl+C
            except KeyboardInterrupt:
                break

    def mySerialDecode(self):
      ''' функция возвращает список переменных разделенных \n '''
      data = "0"
 
      time.sleep(0.2)      
      serialline = self.ser.readline().split('\n')
       
      if serialline:
            data = serialline
                   
      return data