from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from exams_api.models import ExamSheet, Exam, MarksRange, TaskSheet, Task
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
        self.exam_attrs_1 = dict(user=self.user, exam_sheet=self.examsheet_1)
        self.exam_1 = Exam.objects.create(**self.exam_attrs_1)

        self.examsheet_2 = ExamSheet.objects.create(
            title="Test exam 2",
            creator=self.user,
            max_score=100,
            marks_range=self.range,
        )
        self.task_sheet_attrs_1 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_2,
            creator=self.user,
            score=20,
            answer='2'
        )
        self.task_sheet_attrs_2 = dict(
            question='2+2= ?',
            exam_sheet=self.examsheet_2,
            creator=self.user,
            score=30,
            answer='4'
        )
        self.task_sheet_attrs_3 = dict(
            question='3+2= ?',
            exam_sheet=self.examsheet_2,
            creator=self.user,
            score=50,
            answer='5'
        )
        self.task_sheet_1 = TaskSheet.objects.create(**self.task_sheet_attrs_1)
        self.task_sheet_2 = TaskSheet.objects.create(**self.task_sheet_attrs_2)
        self.task_sheet_3 = TaskSheet.objects.create(**self.task_sheet_attrs_3)

        self.task_attrs_1 = dict(
            user=self.user,
            task_sheet=self.task_sheet_1,
            answer='2',
        )
        self.task_attrs_2 = dict(
            user=self.user,
            task_sheet=self.task_sheet_2,
            answer='4',
        )
        self.task_1 = Task.objects.create(**self.task_attrs_1)
        self.task_2 = Task.objects.create(**self.task_attrs_2)

        self.exam_attrs_2 = dict(user=self.user, exam_sheet=self.examsheet_2)
        self.exam_2 = Exam.objects.create(**self.exam_attrs_2)

    def test_exam_str(self):
        self.assertEqual(self.exam_1.__str__(), f'ExamSheet: {self.examsheet_1} for user test0')

    def test_exam_score_property(self):
        self.assertEqual(self.exam_1.score, 0)
        self.assertEqual(self.exam_2.score, 50.0)

    def test_exam_progress_property(self):
        self.assertEqual(self.exam_1.progress, "0/0")
        self.assertEqual(self.exam_2.progress, "2/3")

    def test_check_final_grade(self):
        from exams_api.helpers.models_helpers import check_final_grade
        self.assertEqual(check_final_grade(self.range, 5), 'Non-Certification')
        self.assertEqual(check_final_grade(self.range, 15), 'Very bad')
        self.assertEqual(check_final_grade(self.range, 35), 'Bad')
        self.assertEqual(check_final_grade(self.range, 55), 'Moderate')
        self.assertEqual(check_final_grade(self.range, 75), 'Good')
        self.assertEqual(check_final_grade(self.range, 95), 'Very good')

    def test_final_grade(self):
        self.assertEqual(self.exam_1.final_grade, "Marks range is not defined for this Exam Sheet.")
        self.assertEqual(self.exam_2.final_grade, "Complete all tasks at this Exam Sheet to see your final grade.")
