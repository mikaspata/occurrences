import datetime

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User


class OccurenceState(models.Model):
    """
    1 - Por validar
    2 - Validado
    3 - Resolvido
    """
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class OccurenceCategory(models.Model):
    """
    1 - CONSTRUCTION: planned road work
    2 - SPECIAL_EVENT: special events (fair, sport event, etc.)
    3 - INCIDENT: accidents and other unexpected events
    4 - WEATHER_CONDITION: weather condition affecting the road
    5 - ROAD_CONDITION: status of the road that might affect travellers (potholes, bad pavement, etc.)
    """
    label = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.label
    

class Occurence(models.Model):
    description = models.CharField(max_length=200)
    geo_location = gis_models.PointField(null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    occurence_state = models.ForeignKey(OccurenceState, on_delete=models.DO_NOTHING)
    occurence_category = models.ForeignKey(OccurenceCategory, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('-modified_date',)

    def __str__(self):
        return self.description