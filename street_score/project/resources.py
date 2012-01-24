from djangorestframework import views
from djangorestframework import resources
from . import models


##
# The definition of a rating resource, and its corresponding views.
#

class RatingResource (resources.ModelResource):
    model = models.Rating
    exclude = ['created_datetime', 'updated_datetime']
    include = ['url']

    def criterion(self, rating):
        return rating.criterion.id

    def segment(self, rating):
        return rating.segment.id

class RatingInstanceView (views.InstanceModelView):
    resource = RatingResource

class RatingListView (views.ListOrCreateModelView):
    resource = RatingResource


##
# The definition of a survey session resource, and its view.
#

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
