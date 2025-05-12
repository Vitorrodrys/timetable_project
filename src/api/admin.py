from django.contrib import admin

from . import models

admin.site.register(models.Course)
admin.site.register(models.CourseSection)
admin.site.register(models.Environment)
admin.site.register(models.Professor)
admin.site.register(models.Subject)
