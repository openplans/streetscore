import math
import random
from django.db import models


class TimeStampedModel (models.Model):
    """
    Base model class for when you want to keep track of created and updated
    times for model instances.

    """
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rating (TimeStampedModel):
    criterion = models.ForeignKey('Criterion', related_name='ratings')
    """ The criterion that this rating is for.
        """

    place1 = models.ForeignKey('Place', related_name='+')
    """ The first place that this rating compares
        """

    place2 = models.ForeignKey('Place', related_name='+')
    """ The second place that this rating compares
        """

    score = models.IntegerField()
    """ The rating score.  1 means that place1 "wins" over place2 for the given
        criterion.  -1 means that place2 "wins".
        """

    user_info = models.ForeignKey('UserInfo', null=True, related_name='ratings')
    """ The information for the user that made this rating.  Not required, but
        useful for data analysis.
        """

    def __unicode__(self):
        meaning = ({
            -1: 'more {0} than',
            1:  'less {0} than',
            0:  'as {0} as',
        })

        return ('Place #{p1} is {rating} place #{p2}').format(
                p1=self.place1, p2=self.place2,
                rating=meaning[self.score].format(self.criterion.prompt))

    @property
    def question(self):
        """
        The question string to which the rating is a response.
        """
        return self.criterion.prompt


class Criterion (models.Model):
    prompt = models.TextField()
    """ The question prompt, i.e. 'How clean is the street?'.
        """

    def __unicode__(self):
        return self.prompt

    class Meta:
        verbose_name_plural = "criteria"


class Place (models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __unicode__(self):
        return '({0}, {1})'.format(self.lat, self.lon)


class UserInfo (TimeStampedModel):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    """ The user's location.
        """

    SOURCES = (
        ('ip', 'IP Address'),
        ('html5', 'HTML5 Geolocation API'),
    )
    location_source = models.CharField(max_length=32, choices=SOURCES)
    location_data = models.CharField(max_length=2048)
    """ The method by which the location was obtained, and any additional
        information required to recreate the location.
        """

    session = models.OneToOneField('sessions.Session')
    """ The Django browser session.
        """


class SurveySession (object):
    """

    """

    def __init__(self, questions=None, places=None):
        self.__questions = questions
        self.__places = places

    @property
    def questions(self):
        """
        Get the set of questions for this survey.
        """
        return self.__questions or self.init_questions()

    @property
    def places(self):
        """
        Get the block for this session.
        """
        return self.__places or self.init_places()

    def init_places(self):
        """
        Load two places at random.

        TODO: Order the places by those that have the least questions answered
              about them first.
        """
        places = Place.objects.all().order_by('?')[:2]

        self.__places = places
        return self.__places

    def init_questions(self):
        """
        Load a set of questions at random.
        """
        all_questions = (
            Criterion.objects.all()
                .annotate(num_ratings=models.Count('ratings'))
        )
        self.__questions = all_questions
        return self.__questions

    @classmethod
    def make_surveys(cls, count=1):
        # TODO: Choose the places and questions more smartly.  Use the init_...
        #       methods defined above (and make them better too).
        places = list(Place.objects.all().order_by('?')[:(count * 2)])
        questions = list(Criterion.objects.all())
        surveys = []

        for i in range(count):
            place1 = places[2 * i]
            place2 = places[2 * i + 1]

            surveys.append(cls(places=[place1, place2], questions=questions))

        return surveys
