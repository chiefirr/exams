from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import MarksRange
from exams_api.serializers import MarksRangekBaseSerializer


class MarksRangeSerializerTests(TestCase):

    def setUp(self):
        self.range = MarksRange.objects.create(very_bad=10,
                                               bad=20,
                                               moderate=50,
                                               good=70,
                                               very_good=85
                                               )

        self.attrs = dict(very_bad=1,
                          bad=1,
                          moderate=1,
                          good=1,
                          very_good=1)

        self.range_bad = MarksRange.objects.create(**self.attrs)

    def test_contains_expected_fields_marksrange_serializer(self):
        serializer = MarksRangekBaseSerializer(data=self.range)
        self.assertCountEqual(serializer.fields, {'id', 'very_bad', 'bad', 'moderate', 'good', 'very_good'})

    def test_range_validation(self):
        serializer = MarksRangekBaseSerializer(data=self.range_bad)
        self.assertFalse(serializer.is_valid())

    def test_range_validation_attrs(self):
        serializer = MarksRangekBaseSerializer(data=self.range_bad)
        with self.assertRaises(ValidationError) as context:
            serializer.validate(self.attrs)
        self.assertEqual(context.exception.detail[0].__str__(), "Your ranges are not sorted ascendingly.")
