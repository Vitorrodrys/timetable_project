from django.db import models


class TimeSlot(models.Model):
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()


class TimeSlotSchema(models.Model):
    name = models.CharField(max_length=100)
    time_slots = models.ManyToManyField(TimeSlot)
