from django.contrib.gis import admin
from . import models

admin.site.register(models.Criterion)
admin.site.register(models.Rating)
admin.site.register(models.Segment, admin.GeoModelAdmin)
