from typing import ClassVar
from django.db import models
import datetime
from django.utils import timezone

class Entradas(models.Model):
    alunos = models.IntegerField()
    temperatura = models.FloatField()
    lux = models.FloatField()
    humidade = models.FloatField()
    voltagem = models.FloatField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Adjust timezone if necessary
        delayed_time = self.data - timezone.timedelta(hours=3)
        return delayed_time.strftime('%Y-%m-%d %H:%M:%S')
