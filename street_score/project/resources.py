from djangorestframework import views
from djangorestframework import resources
from . import models

class RatingResource (resources.ModelResource):
    model = models.Rating

class RatingInstanceView (views.InstanceModelView):
    resource = RatingResource

class RatingListView (views.ListOrCreateModelView):
    resource = RatingResource

class SurveySessionView (views.View):
    def get(self, request, *args, **kwargs):
        # super(SurveySessionView, self).get(request, *args, **kwargs)
