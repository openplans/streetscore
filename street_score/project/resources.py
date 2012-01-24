from djangorestframework import mixins
from djangorestframework import parsers
from djangorestframework import resources
from djangorestframework import views
from . import models


##
# The definition of a rating resource, and its corresponding views.
#

class RatingResource (resources.ModelResource):
    model = models.Rating
    exclude = ['created_datetime', 'updated_datetime']
    include = ['question']

    def criterion(self, rating):
        return rating.criterion.id

    def segment(self, rating):
        return rating.segment.id

class RatingJSONParser (parsers.JSONParser):
    def parse(self, stream):
        parsed_data, parsed_files = super(RatingJSONParser, self).parse(stream)

        # Backbone.js likes to send up all the data in a model, whether you want
        # it to or not.  This means that we get attributes that we don't want,
        # like `id` and `url`.  Here, we're ignoring those attributes.
        #
        # I don't like this as a solution; I feel like I should be able to
        # clean my data on the client before saving (without having to override
        # the entire sync method).  I may have to extend the Backbone.Model
        # class to be a little smarter.

        if u'id' in parsed_data:
            del parsed_data[u'id']
        if u'url' in parsed_data:
            del parsed_data[u'url']
        if u'question' in parsed_data:
            del parsed_data[u'question']

        return parsed_data, parsed_files

class RatingInstanceView (views.InstanceModelView):
    parsers = [parser for parser in parsers.DEFAULT_PARSERS
               if parser is not parsers.JSONParser]
    parsers.insert(0, RatingJSONParser)

    resource = RatingResource

class RatingListView (views.ListOrCreateModelView):
    resource = RatingResource


class BlockRatingListView (mixins.PaginatorMixin, views.ListModelView):
    resource = RatingResource

    @property
    def queryset(self):
        return models.Rating.objects.order_by('segment', 'block_index')

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
        block_index = request.GET.get('block_index')
        segment_id = request.GET.get('segment')

        block = None
        if segment_id is not None and block_index is not None:
            segment = models.Segment.objects.get(segment_id)
            block = models.Block(segment, int(block_index))

        survey_session = models.SurveySession(block=block)
        return SurveySessionResource().serialize_model(survey_session)
