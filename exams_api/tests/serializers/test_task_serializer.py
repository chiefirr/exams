from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import Task, MarksRange, ExamSheet, Exam, TaskSheet
from exams_api.serializers import TaskBaseSerializer

User = get_user_model()


class MarksRangeSerializerTests(TestCase):

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
            username='test2',
            email='test2@test2.test2',
            password='super_epic_test_pass'
        )

        self.examsheet_1 = ExamSheet.objects.create(
            title="Test exam 1",
            creator=self.user,
            max_score=100,
        )
        self.exam_attrs_1 = dict(user=self.user, exam_sheet=self.examsheet_1)
        self.exam_1 = Exam.objects.create(**self.exam_attrs_1)

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
            score=50,
            answer='4'
        )

        self.task_sheet_2 = TaskSheet.objects.create(**self.task_sheet_attrs_2)

        self.task_attrs_1 = dict(
            user=self.user,
            task_sheet=self.task_sheet_1,
            answer='2',
            score=20
        )
        self.task_1 = Task.objects.create(**self.task_attrs_1)

        self.task_attrs_2 = dict(
            user=self.user,
            task_sheet=self.task_sheet_2.pk,
            answer='2',
            score=20
        )

        class MockupRequest:
            def __init__(self, user):
                self.user = user

        self.context_1 = {'request': MockupRequest(self.user)}
        self.context_2 = {'request': MockupRequest(self.user_bad)}

    def test_contains_expected_fields_marksrange_serializer(self):
        serializer = TaskBaseSerializer(data=self.task_1)
        self.assertCountEqual(serializer.fields, {'id', 'user', 'task_sheet', 'answer', 'right_answer'})

    def test_save_serializer(self):
        serializer = TaskBaseSerializer(data=self.task_attrs_2, context=self.context_2)
        with self.assertRaises(ValidationError) as context:
            serializer.save()
        self.assertEqual(context.exception.detail[0].__str__(),
                         "You did not create an Exam which contains this Task Sheet. You can't answer this Task Sheet now.")

    def test_save_serializer_success(self):
        serializer = TaskBaseSerializer(data=self.task_attrs_2, context=self.context_1)
        count_ctr = Task.objects.all().count()
        serializer.is_valid()
        serializer.save()
        self.assertEqual(Task.objects.all().count(), count_ctr + 1)
