from djangorestframework import views
from djangorestframework import resources
from . import models

class RatingResource (resources.ModelResource):
    model = models.Rating

    @property
    def question(self, rating):
        return rating.criterion.prompt

class RatingInstanceView (views.InstanceModelView):
    resource = RatingResource

class RatingListView (views.ListOrCreateModelView):
    resource = RatingResource


class SurveySessionResource (resources.Resource):

    model = models.SurveySession  # Can I get away with this?
    fields = (
        'questions',
        'segment_id',
        'block_index',
        'point'
    )

    def questions(self, session):
        return session.questions

    def segment_id(self, session):
        return session.block.segment.id

    def block_index(self, session):
        return session.block.index

    def point(self, session):
        p = session.block.characteristic_point
        return { 'lat': p.y, 'lon': p.x }

class SurveySessionView (views.View):
    def get(self, request):
        survey_session = models.SurveySession()
        return SurveySessionResource().serialize_model(survey_session)
