from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=50)
    address = models.GenericIPAddressField()

    def __str__(self):
        return self.name

