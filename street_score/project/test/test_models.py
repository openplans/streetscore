from django.test import TestCase
from nose.tools import *

from ..models import Criterion, Rating, Place

class RatingModelTest (TestCase):

    def setUp(self):
        super(RatingModelTest, self).setUp()

        Place.objects.all().delete()
        Rating.objects.all().delete()

    def test_unicode_conversion (self):
        """Make sure that the unicode conversion of a rating runs."""
        criterion = Criterion.objects.create(prompt='robust')
        place1 = Place.objects.create(lat=1, lon=2)
        place2 = Place.objects.create(lat=3, lon=4)

        rating1 = Rating.objects.create(criterion=criterion, place1=place1, place2=place2, score=-1)
        assert_equal(unicode(rating1), 'Place #(1, 2) is more robust than place #(3, 4)')

        rating2 = Rating.objects.create(criterion=criterion, place1=place1, place2=place2, score=1)
        assert_equal(unicode(rating2), 'Place #(1, 2) is less robust than place #(3, 4)')

        rating3 = Rating.objects.create(criterion=criterion, place1=place1, place2=place2, score=0)
        assert_equal(unicode(rating3), 'Place #(1, 2) is as robust as place #(3, 4)')
