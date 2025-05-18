from django.contrib import admin

from . import models

admin.site.register(models.Course)
admin.site.register(models.Discipline)
admin.site.register(models.Environment)
admin.site.register(models.Professor)
admin.site.register(models.SchoolClass)
admin.site.register(models.TimeSlot)
admin.site.register(models.TimeSlotSchema)
