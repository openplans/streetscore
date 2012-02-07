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

        ignore = [u'id', u'url', u'question', u'point']
        for key in ignore:
            if key in parsed_data:
                del parsed_data[key]

        return parsed_data, parsed_files


class RatingInstanceView (views.InstanceModelView):
    parsers = [parser for parser in parsers.DEFAULT_PARSERS
               if parser is not parsers.JSONParser]
    parsers.insert(0, RatingJSONParser)

    resource = RatingResource


class RatingListView (mixins.PaginatorMixin, views.ListOrCreateModelView):
    resource = RatingResource

    @property
    def queryset(self):
        return models.Rating.objects.order_by('segment', 'block_index').select_related()


class BlockRatingResource (RatingResource):
    model = models.Rating
    exclude = ['created_datetime', 'updated_datetime', 'score', 'segment__id']
    include = ['segment', 'question', 'point', 'score__avg']

    def segment(self, rating):
        return rating['segment__id']

    def point(self, rating):
        segment = models.Segment.objects.get(id=rating['segment__id'])
        block = models.Block(segment, rating['block_index'])
        p = block.characteristic_point
        return {'lat': p.y, 'lon': p.x}

    def question(self, rating):
        return rating['criterion__prompt']


class BlockRatingListView (mixins.PaginatorMixin, views.ListModelView):
    resource = BlockRatingResource

    @property
    def queryset(self):
        from django.db.models import Avg
        return models.Rating.objects.values('segment__id', 'block_index', 'criterion__prompt').annotate(Avg('score')).select_related()


##
# The definition of a survey session resource, and its view.
#
class SurveySessionResource (resources.Resource):
    model = models.SurveySession  # Can I get away with this?

    fields = (
        'questions',
        'blocks'
    )

    def questions(self, session):
        return session.questions

    def blocks(self, session):
        blocks_data = []
        for block in session.blocks:
            p = block.characteristic_point
            block_data = {
                'segment_id': block.segment.id,
                'block_index': block.index,
                'point': {'lat': p.y, 'lon': p.x}
            }
            blocks_data.append(block_data)

        return blocks_data


class SurveySessionView (views.View):
    def get(self, request):
        # block_index = request.GET.get('block_index')
        # segment_id = request.GET.get('segment')

        blocks = None
        # if segment_id is not None and block_index is not None:
        #     segment = models.Segment.objects.get(segment_id)
        #     block = models.Block(segment, int(block_index))

        survey_session = models.SurveySession(blocks=blocks)
        return SurveySessionResource().serialize_model(survey_session)


class SurveySessionListView (views.View):
    def get(self, request):
        count = int(request.GET.get('count', 2))
        return [SurveySessionResource().serialize_model(s)
            for s in models.SurveySession.make_surveys(count)]
