# coding: utf-8
from django.core.management import BaseCommand
import zmq
import consts
from core import models


class Command(BaseCommand):
    help = 'Test car socket connect'

    def add_arguments(self, parser):
        parser.add_argument('car_name', nargs='*', default=['local'])

    def handle(self, *args, **options):
        car_name = options['car_name'][0]
        car = models.Car.objects.get(name=car_name)
        ping_server_address = 'tcp://%s:%s' % (car.address, consts.CAR_COMMAND_SERVER_PORT)

        print('Try to connect to %s to %s...' % (car, ping_server_address))
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(ping_server_address)
        print('Connected to %s successfully!' % car)

        while True:
            msg = input('Enter ping message: ')
            socket.send_string(msg)

            response = socket.recv_string()
            print('Get response: %s' % response)

