from django.contrib.auth import get_user_model
from django.test import TestCase

from exams_api.models import TaskSheet, Task, ExamSheet

User = get_user_model()


class TaskModelTests(TestCase):
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

        self.task_sheet_attrs_1 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_1,
            creator=self.user,
            score=30,
            answer='2'
        )

        self.task_sheet_1 = TaskSheet.objects.create(**self.task_sheet_attrs_1)

        self.task_attrs = {
            'user': self.user,
            'task_sheet': self.task_sheet_1,
            'answer': 2,
            'score': 10,
            'pk': 1
        }

    def test_should_return_task_name(self):
        examsheet = Task(**self.task_attrs)
        assert examsheet.__str__() == f"Task 1 finished by user {self.user}"
