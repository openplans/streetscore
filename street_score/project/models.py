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

    segment1 = models.ForeignKey('Segment', related_name='+')
    block1_index = models.PositiveIntegerField()
    """ The first block that this rating compares. A segment and a block_index together
        uniquely identify a Block. Not including a related_name until needed. Tricky.
        """

    segment2 = models.ForeignKey('Segment', related_name='+')
    block2_index = models.PositiveIntegerField()
    """ The second block that this rating compares. A segment and a block_index together
        uniquely identify a Block. Not including a related_name until needed. Tricky.
        """

    score = models.PositiveIntegerField()
    """ The rating score.
        """

    def __unicode__(self):
        return 'Rating of Segment #{0}, block #{1} for "{2}"'.format(
            self.segment.id, self.block_index, self.criterion.prompt)

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
        return 'Segement #{0}'.format(self.id)

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

    def __init__(self, questions=None, blocks=None):
        self.__questions = questions
        self.__blocks = blocks

    @property
    def questions(self):
        """
        Get the set of questions for this survey.
        """
        return self.__questions or self.init_questions()

    @property
    def blocks(self):
        """
        Get the block for this session.
        """
        return self.__blocks or self.init_blocks()

    def init_blocks(self):
        """
        Load two blocks at random.

        TODO: Order the blocks by those that have the least questions answered
              about them first.
        """
        ten_least_rated_segments = (
            Segment.objects.all()[:10]
        )

        segments = random.sample(ten_least_rated_segments, 2)
        self.__blocks = [random.choice(segment.blocks) for segment in segments]
        return self.__blocks

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
