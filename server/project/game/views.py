# -*-coding:utf8 -*-
import socket
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render


def control_game(request):
    c = {}
    url_ajax_switch = reverse('game.views.switch_for_arduino')
    c['url_ajax_switch'] = url_ajax_switch
    return render(request, 'game/control_game.html', c)


def switch_for_arduino(request):
    print 'dsf'
    print request
    if request.is_ajax() and request.method == 'POST':
        toggle = request.POST['toggle']
        arduino_send_command(toggle)
        return HttpResponse(toggle)


def arduino_send_command(toggle):
    '''
    :param toggle: параметр, который мы отправляем на ардуино
    :return:
    '''
    import serial

    #открываем порт
    #я питон запускал через судо
    port = '/dev/ttyACM0'
    ser = serial.Serial(port, 9600, dsrdtr = 1,timeout = 0)

    ser.write(toggle)


def get_socket(port):
    sock = socket.socket()
    sock.bind(('0.0.0.0', port))
    sock.listen(1) #кол-во слушателей

    conn, addr = sock.accept() #принимаем подключение, как только его примет пойдем дальше
    print 'connected:', addr
    return sock