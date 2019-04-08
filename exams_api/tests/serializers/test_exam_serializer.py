from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import ExamSheet, Exam, MarksRange, TaskSheet
from exams_api.serializers import ExamBaseSerializer

User = get_user_model()


class ExamSerializerTests(TestCase):

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

        self.examsheet_2 = ExamSheet.objects.create(
            title="Test exam 5",
            creator=self.user,
            max_score=100,
        )

        self.examsheet_3 = ExamSheet.objects.create(
            title="Test exam 7",
            creator=self.user,
            max_score=100,
        )

        self.task_sheet_attrs_2 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_2,
            creator=self.user,
            score=30,
            answer='2'
        )
        self.task_sheet_2 = TaskSheet.objects.create(**self.task_sheet_attrs_2)

        self.task_sheet_attrs_3 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_3,
            creator=self.user,
            score=50,
            answer='2'
        )
        self.task_sheet_3 = TaskSheet.objects.create(**self.task_sheet_attrs_3)

        self.task_sheet_attrs_4 = dict(
            question='2+2= ?',
            exam_sheet=self.examsheet_3,
            creator=self.user,
            score=50,
            answer='2'
        )
        self.task_sheet_4 = TaskSheet.objects.create(**self.task_sheet_attrs_4)

        self.exam_attrs_1 = dict(user=self.user, exam_sheet=self.examsheet_1)
        self.exam_attrs_2 = dict(user=self.user, exam_sheet=self.examsheet_2)
        self.exam_attrs_3 = dict(user=self.user, exam_sheet=self.examsheet_3)
        self.exam_1 = Exam.objects.create(**self.exam_attrs_1)
        self.exam_2 = Exam.objects.create(**self.exam_attrs_2)
        self.exam_3 = Exam.objects.create(**self.exam_attrs_3)

        Obj = namedtuple('Obj', 'score')
        self.obj = Obj(score=20)

        Obj2 = namedtuple('Obj2', 'exam_sheet')
        self.exam_sheet_mokup = Obj2(exam_sheet=self.examsheet_1)

    def test_contains_expected_fields_exam_serializer(self):
        serializer1 = ExamBaseSerializer(data=self.exam_1)
        self.assertCountEqual(serializer1.fields, {'id', 'user', 'exam_sheet', 'score', 'progress', 'final_grade'})

    def test_score_validation(self):
        serializer = ExamBaseSerializer(data=self.exam_1)
        self.assertEqual(serializer.get_score(self.obj), '20%')

    def test_get_exam_sheet(self):
        from exams_api.serializers import ExamSheetBaseSerializer
        serializer = ExamBaseSerializer(data=self.exam_1)
        self.assertEqual(serializer.get_exam_sheet(self.exam_sheet_mokup),
                         ExamSheetBaseSerializer(self.examsheet_1).data)

    def test__validation(self):
        serializer = ExamBaseSerializer(data=self.exam_1)
        with self.assertRaises(ValidationError) as context:
            serializer.validate(self.exam_attrs_1)
        self.assertEqual(context.exception.detail[0].__str__(), "Ooops! This exam has no tasks! Try another one!")

        serializer = ExamBaseSerializer(data=self.exam_2)
        with self.assertRaises(ValidationError) as context:
            serializer.validate(self.exam_attrs_2)
        self.assertEqual(context.exception.detail[0].__str__(),
                         "Sorry, you can't start this exam - its max score is not reached yet. Ask the author: 'test0' to add more questions. Missing: 70 points.")

        serializer = ExamBaseSerializer(data=self.exam_3)
        self.assertDictEqual(serializer.validate(self.exam_attrs_3), self.exam_attrs_3)
