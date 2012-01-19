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


class Segment (models.Model):
    class Meta:
        db_table = u'xxx'

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
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    @property
    def center_point(self):
        """
        The half-way point between the beginning and end of the block.
        """
