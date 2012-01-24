import math
import random
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


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

    segment = models.ForeignKey('Segment', related_name='ratings')
    block_index = models.PositiveIntegerField()
    """ The block that this rating scores. A segment and a block_index together
        uniquely identify a Block.
        """

    score = models.PositiveIntegerField()
    """ The rating score.
        """

    @property
    def block(self):
        """
        The block that this rating scores. The block is identified by the
        segment and block_index for the rating.
        """
        return Block(self.segment, self.block_index)

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


class Segment (models.Model):
    id = models.IntegerField(db_column='osm_id', primary_key=True)
    way = models.LineStringField(srid=900913, null=True)

    objects = models.GeoManager()

    class Meta:
        db_table = u'philly_street_osm_line'
        managed = False

    def __unicode__(self):
        return 'Segement #{}'.format(self.id)

    @property
    def blocks(self):
        """
        The blocks that fall along the segment.  If the segment is shorter than
        the block length, it will contain only one block.
        """
        class BlockSet (object):
            def __init__(self, segment):
                self.segment = segment

            def __len__(self):
                return int(math.ceil(self.segment.way.length / Block.MAX_LENGTH))

            def __getitem__(self, n):
                return Block(self.segment, n)

        return BlockSet(self)


class Block (object):
    MAX_LENGTH = 200.0

    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    @property
    def _start_interpolation(self):
        return (self.MAX_LENGTH * self.index) / self.segment.way.length

    @property
    def length(self):
        return min(self.segment.length - (self.index * self.MAX_LENGTH), self.MAX_LENGTH)

    @property
    def characteristic_point(self):
        """
        The a point that will represent the block (not necessarily uniquely).
        """
        point_data = Segment.objects.raw(
            ('SELECT *, ST_transform(ST_line_interpolate_point(way, %s), 4326) '
                 'AS q_start_point '
             'FROM philly_street_osm_line WHERE osm_id=%s'),
            [self._start_interpolation, self.segment.id])[0].q_start_point
        point = GEOSGeometry(point_data)
        return point


class SurveySession (object):
    """

    """

    def __init__(self, questions=None, block=None):
        self.__questions = questions
        self.__block = block

    @property
    def questions(self):
        """
        Get the set of questions for this survey.
        """
        return self.__questions or self.init_questions()

    @property
    def block(self):
        """
        Get the block for this session.
        """
        return self.__block or self.init_block()

    def init_block(self):
        """
        Load a block at random.

        TODO: Order the blocks by those that have the least questions answered
              about them first.
        """
        ten_least_rated_segments = (
            Segment.objects.all()
                .annotate(num_ratings=models.Count('ratings'))
                .order_by('num_ratings')[:10]
        )

        segment = random.choice(ten_least_rated_segments)
        self.__block = random.choice(segment.blocks)
        return self.__block

    def init_questions(self):
        """
        Load a set of questions at random.
        """
        ten_least_answered_questions = (
            Criterion.objects.all()
                .annotate(num_ratings=models.Count('ratings'))
                .order_by('num_ratings')[:10]
        )
        self.__questions = random.sample(ten_least_answered_questions, 2)
        return self.__questions
