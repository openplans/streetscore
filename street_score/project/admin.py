from django.contrib.gis import admin
from . import models

class RatingAdmin (admin.ModelAdmin):
    list_select_related = True

admin.site.register(models.Criterion)
admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.Segment, admin.GeoModelAdmin)
