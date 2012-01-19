from django.contrib.gis.db import models


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
    way = models.LineStringField(srid=900913)

    objects = models.GeoManager()

    class Meta:
        db_table = u'philly_street_osm_line'

    def __unicode__(self):
        return 'Segement #{}'.format(self.id)

    @property
    def blocks(self):
        """
        The blocks that fall along the segment.  If the segment is shorter than
        the block length, it will contain only one block.
        """
        []

    def block(index):
        """
        The index-th block along the segment. ValueError if index is too large.
        """
        raise ValueError()


class Block (object):
    MAX_LENGTH = 0.2

    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    @property
    def characteristic_point(self):
        """
        The half-way point between the beginning and end of the block.
        """


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
        """
        segment = random.choice(Segment.objects.all())
        self.__block = random.choice(segment.blocks)
        return self.__block

    def init_questions(self):
        """
        Load a set of questions at random.
        """
        self.__questions = random.sample(Criterion.objects.all(), 2)
        return self.__questions
