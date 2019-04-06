import datetime

from django.test import TestCase

from exams_api.models import MarksRange


class MarksRangeTests(TestCase):
    def setUp(self):
        self.range_dict = {
            'very_bad': 11,
            'bad': 22,
            'moderate': 33,
            'good': 44,
            'very_good': 55,
            'pk': 1
        }

    def test_should_return_marksrange_pk(self):
        rangez = MarksRange(**self.range_dict)
        assert rangez.__str__() == f"MarksRange: 1"
