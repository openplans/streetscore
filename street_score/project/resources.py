from djangorestframework import mixins
from djangorestframework import parsers
from djangorestframework import renderers
from djangorestframework import resources
from djangorestframework import views
from . import models


class UncachedMixin (object):
    def final(self, request, response, *args, **kwargs):
        response.headers['Expires'] = -1
        return super(UncachedMixin, self).final(request, response, *args, **kwargs)


class UserInfoResource (resources.ModelResource):
    model = models.UserInfo
    exclude = ['created_datetime', 'updated_datetime', 'session']


class UserInfoJSONParser (parsers.JSONParser):
    def parse(self, stream):
        parsed_data, parsed_files = super(UserInfoJSONParser, self).parse(stream)

        # Backbone.js likes to send up all the data in a model, whether you want
        # it to or not.  This means that we get attributes that we don't want,
        # like `id` and `url`.  Here, we're ignoring those attributes.
        #
        # I don't like this as a solution; I feel like I should be able to
        # clean my data on the client before saving (without having to override
        # the entire sync method).  I may have to extend the Backbone.Model
        # class to be a little smarter.

        ignore = [u'id', u'url']
        for key in ignore:
            if key in parsed_data:
                del parsed_data[key]

        return parsed_data, parsed_files


class UserInfoInstanceView (UncachedMixin, views.InstanceModelView):
    # Use the UserInfoJSONParser instead of the default JSONParser.
    parsers = [parser for parser in parsers.DEFAULT_PARSERS
               if parser is not parsers.JSONParser]
    parsers.insert(0, UserInfoJSONParser)

    renderers = [renderers.JSONRenderer]
    resource = UserInfoResource


##
# The definition of a rating resource, and its corresponding views.
#

class RatingResource (resources.ModelResource):
    model = models.Rating
    exclude = ['created_datetime', 'updated_datetime']
    include = ['question']


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

        ignore = [u'id', u'url', u'question']
        for key in ignore:
            if key in parsed_data:
                del parsed_data[key]

        return parsed_data, parsed_files


class RatingInstanceView (UncachedMixin, views.InstanceModelView):
    # Use the RatingJSONParser instead of the default JSONParser.
    parsers = [parser for parser in parsers.DEFAULT_PARSERS
               if parser is not parsers.JSONParser]
    parsers.insert(0, RatingJSONParser)

    renderers = [renderers.JSONRenderer]
    resource = RatingResource


class RatingListView (UncachedMixin, mixins.PaginatorMixin, views.ListOrCreateModelView):
    renderers = [renderers.JSONRenderer]
    resource = RatingResource


##
# The definition of a survey session resource, and its view.
#
class SurveySessionResource (resources.Resource):
    model = models.SurveySession  # Can I get away with this?

    fields = (
        'questions',
        'places'
    )

    def questions(self, session):
        return session.questions

    def places(self, session):
        return session.places


class SurveySessionListView (UncachedMixin, views.View):
    renderers = [renderers.JSONRenderer]

    def get(self, request):
        count = int(request.GET.get('count', 5))
        return [SurveySessionResource().serialize_model(s)
            for s in models.SurveySession.make_surveys(count)]
