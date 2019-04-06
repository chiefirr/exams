from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import ExamSheet, MarksRange, TaskSheet
from exams_api.serializers import TaskSheetBaseSerializer

User = get_user_model()


class TaskSheetSerializerTests(TestCase):

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

        self.user_bad = User.objects.create_user(
            username='test1',
            email='test2@test2.test2',
            password='super_epic_test_pass2'
        )

        self.examsheet_1 = ExamSheet.objects.create(
            title="Test exam 1",
            creator=self.user,
            max_score=100,
        )

        self.examsheet_2 = ExamSheet.objects.create(
            title="Test exam 2",
            creator=self.user,
            max_score=80,
        )

        self.task_sheet_attrs_1 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_1,
            creator=self.user,
            score=30,
            answer='2'
        )

        self.task_sheet_1 = TaskSheet.objects.create(**self.task_sheet_attrs_1)

        self.task_sheet_attrs_2 = dict(
            question='2+2= ?',
            exam_sheet=self.examsheet_1,
            creator=self.user,
            score=300,
            answer='4'
        )

        self.task_sheet_attrs_3 = dict(
            question='3+3= ?',
            exam_sheet=self.examsheet_2.pk,
            creator=self.user,
            score=22,
            answer='6'
        )

        self.task_sheet_2 = TaskSheet.objects.create(**self.task_sheet_attrs_2)

        self.score = 300

        class MockupRequest:
            def __init__(self, examsheet, user):
                self.data = {'exam_sheet': examsheet.pk}
                self.user = user

        self.context = {'request': MockupRequest(self.examsheet_1, self.user_bad)}
        self.context_2 = {'request': MockupRequest(self.examsheet_2, self.user)}

    def test_contains_expected_fields_examsheets_serializer(self):
        serializer1 = TaskSheetBaseSerializer(data=self.task_sheet_1)
        self.assertCountEqual(serializer1.fields, {'id', 'question', 'creator', 'exam_sheet', 'score', 'answer'})

    def test_score_validation(self):
        serializer = TaskSheetBaseSerializer(data=self.task_sheet_2)
        self.assertFalse(serializer.is_valid())

    def test_score_validation_2(self):
        serializer = TaskSheetBaseSerializer(data=self.task_sheet_2, context=self.context)
        with self.assertRaises(ValidationError) as context:
            serializer.validate_score(self.score)
        self.assertEqual(context.exception.detail[0].__str__(),
                         "This score exceeds maximal allowed Exam Sheet score. Free score points left: -230")

    def test_serializer_save(self):
        serializer = TaskSheetBaseSerializer(data=self.task_sheet_2, context=self.context)
        with self.assertRaises(ValidationError) as context:
            serializer.save()
        self.assertEqual(context.exception.detail[0].__str__(),
                         "You are not creator of this Exam Sheet. You can't add Task Sheets here. Create your own Exam Sheet.")

    def test_save_serializer_success(self):
        serializer = TaskSheetBaseSerializer(data=self.task_sheet_attrs_3, context=self.context_2)
        count_ctr = TaskSheet.objects.all().count()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(TaskSheet.objects.all().count(), count_ctr + 1)
