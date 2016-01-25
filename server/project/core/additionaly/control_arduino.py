# -*- coding:utf-8 -*-
import os
import sys
import serial
import time


class ArduinoControl():
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, 9600, dsrdtr = 1,timeout = 0)

    def arduino_write(self, par):
        self.ser.write(par)

    def printAnalogDat(self):
        while 1:

            #запуск чтения из порта и маршрутизация по файлам
            try:
                print self.mySerialDecode()

            #выход по Ctrl+C
            except KeyboardInterrupt:
                  break

    def mySerialDecode(self):
        data = "0"

        time.sleep(0.2)
        serialline = self.ser.readline().split('\n')

        if serialline[0]:
            data = serialline

        return data