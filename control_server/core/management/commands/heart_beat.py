# coding: utf-8
from django.core.management import BaseCommand
from heart_beat import Heart


class Command(BaseCommand):
    help = 'Start control server hear beating'

    def handle(self, *args, **options):
        heart = Heart()
        try:
            heart.start()
        finally:
            heart.close()
