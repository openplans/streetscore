from djangorestframework import views
from djangorestframework import resources
from . import models

class RatingResource (resources.ModelResource):
    model = models.Rating

class RatingInstanceView (views.InstanceModelView):
    resource = RatingResource

class RatingListView (views.ListOrCreateModelView):
    resource = RatingResource


class SurveySessionResource (resources.Resource):
#    def __init__(self, *args, **kwargs):
#        super(SurveySessionResource, self).__init__(*args, **kwargs)
#        self.survey_session = models.SurveySession()

    model = models.SurveySession  # Can I get away with this?
    fields = (
        'questions',
        'segment_id',
        'block_index',
        'point'
    )

    def segment_id(self, session):
        return session.block.segment.id

    def block_index(self, session):
        return session.block.index

    def point(self, session):
        p = session.block.characteristic_point
        return { 'lat': p.y, 'lon': p.x }

class SurveySessionView (views.View):
    def get(self, request):
        survey_session = SurveySessionResource()
        return survey_session.serialize()
