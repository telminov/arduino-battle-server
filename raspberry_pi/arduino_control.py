import serial
import os
import sys
 
#открываем порт
ser = serial.Serial('COM1', 9600, dsrdtr = 1,timeout = 0) #TODO уточнить порт

#подготовка лог файлов для данных от разных устройств
prgpath = os.path.dirname(os.path.abspath(sys.argv[0]))

#процедура чтения и декодирования строки из порта
def mySerialDecode():
       
      data = "0"
 
      time.sleep(0.2)      
      serialline = ser.readline().split('\n')
       
      if serialline[0]:
            data = serialline;
                   
      return data
 
#процедура передачи данных в порт
#управление авто
def w():
      ser.write('w') 
      print 'w'
 
#проба записать что-то в порт
def s():
      ser.write('s') 
      print 's'

def a():
      ser.write('a') 
      print 'a'

def d():
      ser.write('d') 
      print 'd'

def q():
      ser.write(' ') 
      print ' probel '
 

#вывод значений с аналогового датчика
def printAnalogDat():
      while 1:
             
            #запуск чтения из порта и маршрутизация по файлам
            try:
                 print mySerialDecode()

            #выход по Ctrl+C
            except KeyboardInterrupt:
                  break
  
#закрываем порт
ser.close()