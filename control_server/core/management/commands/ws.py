# coding: utf-8
from django.core.management import BaseCommand

import core.ws


class Command(BaseCommand):
    help = 'Start WebSocket server'

    def handle(self, *args, **options):
        core.ws.start_server()