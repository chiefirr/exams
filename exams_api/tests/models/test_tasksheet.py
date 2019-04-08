import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from exams_api.models import TaskSheet, ExamSheet

User = get_user_model()


class TaskSheetModelTests(TestCase):
    def setUp(self):
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

        self.exam_attrs = {
            'question': '1+1= ?',
            'creator': self.user,
            'exam_sheet': self.examsheet_1,
            'score': 50,
            'answer': 2,
            'pk': 1
        }

    def test_should_return_tasksheet_name(self):
        examsheet = TaskSheet(**self.exam_attrs)
        assert examsheet.__str__() == f"Task 1: to Exam Sheet '{self.examsheet_1}' - Question: '1+1= ?'"
