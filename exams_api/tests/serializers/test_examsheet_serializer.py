from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import ExamSheet, MarksRange
from exams_api.serializers import ExamSheetBaseSerializer

User = get_user_model()


class ExamSheetSerializerTests(TestCase):

    def setUp(self):
        self.range = MarksRange.objects.create(very_bad=10,
                                               bad=20,
                                               moderate=50,
                                               good=70,
                                               very_good=85
                                               )
        self.user = User.objects.create_user(
            username='test0',
            email='test1@test1.test1',
            password='super_epic_test_pass'
        )

        self.examsheet_1 = ExamSheet.objects.create(
            title="Test exam 1",
            creator=self.user,
            max_score=100,
        )

        self.attrs_2 = dict(
            title="Test exam 2",
            creator=self.user,
            max_score=50,
            marks_range=self.range
        )
        self.examsheet_2 = ExamSheet.objects.create(**self.attrs_2)
        MarkR = namedtuple('MarkR', 'very_good')
        self.markcange_instance = MarkR(very_good=100)

    def test_contains_expected_fields_examsheets_serializer(self):
        serializer1 = ExamSheetBaseSerializer(data=self.examsheet_1)
        serializer2 = ExamSheetBaseSerializer(data=self.examsheet_2)
        self.assertCountEqual(serializer1.fields, {'id', 'title', 'creator', 'max_score', 'task_sheets', 'marks_range'})
        self.assertCountEqual(serializer2.fields, {'id', 'title', 'creator', 'max_score', 'task_sheets', 'marks_range'})

    def test_marksrange_validation(self):
        serializer = ExamSheetBaseSerializer(data=self.examsheet_2)
        self.assertFalse(serializer.is_valid())

    def test_range_validation_2(self):
        serializer = ExamSheetBaseSerializer(data=self.attrs_2)
        with self.assertRaises(ValidationError) as context:
            serializer.validate_marks_range(self.markcange_instance)
        self.assertEqual(context.exception.detail[0].__str__(),
                         "Bad marks range for this Exam Sheet. Too high 'very good' mark score.")

    def test_task_sheets(self):
        serializer = ExamSheetBaseSerializer(data=self.examsheet_2)
        # TODO
