# -*-coding:utf8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from core.additionaly.socket_server import SocketServer


def control_game(request):
    c = {}
    url_ajax_switch = reverse('game.views.switch_for_arduino')
    c['url_ajax_switch'] = url_ajax_switch
    return render(request, 'game/control_game.html', c)


def switch_for_arduino(request):
    if request.is_ajax() and request.method == 'POST':
        toggle = request.POST['toggle']
        port = 9090 #TODO передавать сюды порт
        socket_server = get_socket(port)
        print toggle
        socket_server.send_data(toggle)

        return HttpResponse('Good')


def get_socket(port):
    socket_server = SocketServer(port)
    socket_server.accept() #подключается
    return socket_server


def arduino_send_command(toggle):
    '''
    :param toggle: параметр, который мы отправляем на ардуино
    :return:
    '''
    import serial

    #открываем порт
    #я питон запускал через судо
    port = '/dev/ttyACM1'
    ser = serial.Serial(port, 9600, dsrdtr = 1,timeout = 0)

    ser.write(toggle)