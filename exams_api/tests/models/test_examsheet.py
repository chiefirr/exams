import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from exams_api.models import ExamSheet

User = get_user_model()


class ExamSheetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test0',
            email='test1@test1.test1',
            password='super_epic_test_pass'
        )

        self.exam_attrs = {
            'title': 'Test exam title',
            'creator': self.user,
            'max_score': 100,
        }

    def test_should_return_examsheet_title(self):
        examsheet = ExamSheet(**self.exam_attrs)
        assert examsheet.__str__() == f"ExamSheet: Test exam title"
