from django.test import TestCase
from nose.tools import *

from .base import BaseSegmentsTest
from ..models import Criterion, Rating, Segment

class RatingModelTest (BaseSegmentsTest):

    def setUp(self):
        super(RatingModelTest, self).setUp()

        Segment.objects.all().delete()
        Rating.objects.all().delete()

    def test_unicode_conversion (self):
        """Make sure that the unicode conversion of a rating runs."""
        criterion = Criterion.objects.create(prompt='robust')
        segment1 = Segment.objects.create(id=123)
        segment2 = Segment.objects.create(id=456)

        rating1 = Rating.objects.create(criterion=criterion, segment1=segment1, block1_index=0, segment2=segment2, block2_index=0, score=-1)
        assert_equal(unicode(rating1), 'Segment #123, block #0 is more robust than segment #456, block #0')

        rating2 = Rating.objects.create(criterion=criterion, segment1=segment1, block1_index=0, segment2=segment2, block2_index=0, score=1)
        assert_equal(unicode(rating2), 'Segment #123, block #0 is less robust than segment #456, block #0')

        rating3 = Rating.objects.create(criterion=criterion, segment1=segment1, block1_index=0, segment2=segment2, block2_index=0, score=0)
        assert_equal(unicode(rating3), 'Segment #123, block #0 is as robust as segment #456, block #0')
