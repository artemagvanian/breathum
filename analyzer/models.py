import uuid

from django.contrib.auth.models import User
from django.db import models


# TODO: add color to this model
class SensorType(models.Model):
    title = models.CharField(max_length = 150)


class Sensor(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    title = models.CharField(max_length = 150)
    unit = models.CharField(max_length = 30)
    risk_bound = models.FloatField()
    danger_bound = models.FloatField()
    user = models.ManyToManyField(User)
    trust_level = models.DecimalField(max_digits = 1, decimal_places = 0)
    type = models.ForeignKey(SensorType, on_delete = models.CASCADE)


class DataItem(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE)
    data = models.FloatField()
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits = 8, decimal_places = 5)
    longitude = models.DecimalField(max_digits = 8, decimal_places = 5)


class Device(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    sensors = models.ManyToManyField(Sensor)
