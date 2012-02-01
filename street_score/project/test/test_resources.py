from django.test import TestCase
from django.test.client import RequestFactory
from nose.tools import *


class TestRatingResource(TestCase):
    """Tests on RatingResource"""

    def setUp(self):
        super(TestRatingResource, self).setUp()
        from project.models import Segment
        Segment.objects.all().delete()
        self.req = RequestFactory()

    def test_parsers(self):
        from project.resources import RatingInstanceView, RatingJSONParser
        from djangorestframework.parsers import JSONParser
        from StringIO import StringIO

        self.assertEqual(len(RatingInstanceView.parsers), 4)
        self.assertNotIn(JSONParser, RatingInstanceView.parsers)
        self.assertIn(RatingJSONParser, RatingInstanceView.parsers)

        parser = RatingJSONParser(None)  # None for the view
        json_string = StringIO('{"criterion":3,"question":"How much do you like it?","score":"4","segment":456,"block_index":5239,"url":"http://localhost:8000/ratings/13","id":13}')
        self.assertNotIn(u'id', parser.parse(json_string))

    def test_read(self):
        from project.models import Rating, Criterion, Segment
        criterion = Criterion.objects.create(prompt='Hello?')
        segment = Segment.objects.create(id=123)
        rating = Rating.objects.create(criterion=criterion, segment1=segment, block_index1=2, segment2=segment, block_index2=2, score=5)

        from project.resources import RatingInstanceView
        request = self.req.get('/ratings/{}'.format(rating.id))
        view = RatingInstanceView()

        response = view.get(request, rating.id)
        self.assertEquals(rating, response)

    def test_delete(self):
        from project.models import Rating, Criterion, Segment
        criterion = Criterion.objects.create(prompt='Hello?')
        segment = Segment.objects.create(id=123)
        rating = Rating.objects.create(criterion=criterion, segment1=segment, block_index1=2, segment2=segment, block_index2=2, score=5)

        assert_equal(Rating.objects.count(), 1)

        from project.resources import RatingInstanceView
        request = self.req.delete('/ratings/{}'.format(rating.id))
        view = RatingInstanceView()

        response = view.delete(request, rating.id)
        assert_equal(Rating.objects.count(), 0)

    def test_update(self):
        from project.models import Rating, Criterion, Segment
        criterion1 = Criterion.objects.create(prompt='Hello?')
        criterion2 = Criterion.objects.create(prompt='Goodbye!')
        segment1 = Segment.objects.create(id=123)
        segment2 = Segment.objects.create(id=456)
        rating = Rating.objects.create(criterion=criterion1, segment1=segment1, block_index1=2, segment2=segment1, block_index2=2, score=5)

        from project.resources import RatingResource, RatingInstanceView
        request = self.req.put('/ratings/{}'.format(rating.id), data={
            'segment2': segment2.id,
            'block_index2': 14,
            'segment1': segment2.id,
            'block_index1': 14,
            'criterion': criterion2.id,
            'score': 2})
        view = RatingInstanceView()
        view.request = request

        response = view.put(request, rating.id)
        self.assertEquals(rating, response)
        self.assertEqual(response.criterion, criterion2)
        self.assertEqual(response.segment2, segment2)
        self.assertEqual(response.block_index2, 14)
        self.assertEqual(response.score, 2)

    def test_create(self):
        from project.models import Rating, Criterion, Segment
        criterion = Criterion.objects.create(prompt='Hello?')
        segment1 = Segment.objects.create(id=123)
        segment2 = Segment.objects.create(id=456)
        assert_equal(Rating.objects.count(), 0)

        from project.resources import RatingListView
        request = self.req.post('/ratings/', data={
            'segment1': segment1.id,
            'block_index1': 7,
            'segment2': segment2.id,
            'block_index2': 14,
            'criterion': criterion.id,
            'score': 2})
        view = RatingListView()
        view.request = request

        response = view.post(request)
        self.assertEquals(Rating.objects.count(), 1)
        self.assertEqual(response.cleaned_content.criterion, criterion)
        self.assertEqual(response.cleaned_content.segment1, segment1)
        self.assertEqual(response.cleaned_content.block_index1, 7)
        self.assertEqual(response.cleaned_content.score, 2)
