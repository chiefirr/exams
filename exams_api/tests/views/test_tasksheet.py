from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from exams_api.models import ExamSheet, TaskSheet

User = get_user_model()


class TestTaskSheetViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test0',
            email='test1@test1.test1',
            password='qwe111!!!'
        )

        self.exam_attrs = {
            'title': 'Test exam title',
            'creator': self.user,
            'max_score': 100,
        }

        self.user_2 = User.objects.create_user(
            username='test2',
            email='test2@test2.test2',
            password='qwe111!!!'
        )

        self.exam_attrs_2 = {
            'title': 'Test exam title 2',
            'creator': self.user,
            'max_score': 100,
        }

        self.exam_attrs_user_2 = {
            'title': 'Test exam title 2',
            'creator': self.user_2,
            'max_score': 100,
        }

        self.examsheet_1 = ExamSheet.objects.create(**self.exam_attrs)
        self.examsheet_2 = ExamSheet.objects.create(**self.exam_attrs_user_2)

        self.task_sheet_attrs_1 = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_1,
            creator=self.user,
            score=30,
            answer='2'
        )

        self.task_sheet_attrs_exam_pk = dict(
            question='1+1= ?',
            exam_sheet=self.examsheet_1.pk,
            creator=self.user,
            score=10,
            answer='2'
        )
        self.task_sheet_attrs_exam_pk_2 = dict(
            question='3+3= ?',
            exam_sheet=self.examsheet_1.pk,
            creator=self.user,
            score=10,
            answer='6'
        )

        self.task_sheet_attrs_exam_pk_user_2 = dict(
            question='3+3= ?',
            exam_sheet=self.examsheet_2.pk,
            creator=self.user_2,
            score=10,
            answer='6'
        )

        self.task_sheet_attrs_2 = dict(
            question='2+2= ?',
            exam_sheet=self.examsheet_1,
            creator=self.user,
            score=20,
            answer='4'
        )

        self.task_sheet_2 = TaskSheet.objects.create(**self.task_sheet_attrs_2)

    def test_retrieve_tasksheet_object_anon_user(self):
        tasksheet = TaskSheet.objects.create(**self.task_sheet_attrs_1)
        response_retrieve = self.client.get(f'/api/tasks_sheets/{tasksheet.pk}/')
        self.assertEqual(response_retrieve.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_tasksheet_object_anon_user(self):
        taskssheets_count = TaskSheet.objects.all().count()
        response_post = self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_1)

        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(TaskSheet.objects.all().count(), taskssheets_count)

    def test_retrieve_tasksheet_object_loggedin_user(self):
        self.client.login(username='test0', password='qwe111!!!')

        tasksheet = TaskSheet.objects.create(**self.task_sheet_attrs_1)
        response_retrieve = self.client.get(f'/api/tasks_sheets/{tasksheet.pk}/')
        response_retrieve_404 = self.client.get(f'/api/tasks_sheets/{tasksheet.pk + 1}/')
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve_404.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_tasksheet_object(self):
        self.client.login(username='test0', password='qwe111!!!')

        tasksheet_count = TaskSheet.objects.all().count()
        response_post = self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_exam_pk)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskSheet.objects.all().count(), tasksheet_count + 1)

    def test_perform_create_tasksheet_duplicate(self):
        self.client.login(username='test0', password='qwe111!!!')
        self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_exam_pk)

        response = self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_exam_pk)
        self.assertEqual(response.data["error"].__str__(),
                         "This question already exists in this Exam Sheet.")

    def test_tasksheet_user_permissions(self):
        self.client.login(username='test0', password='qwe111!!!')
        response = self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_exam_pk)
        es_pk_1 = response.data['id']

        attrs_edited = dict(
            question='Changed question 1',
            exam_sheet=self.examsheet_1.pk,
            creator=self.user,
            score=15,
            answer='15'
        )
        response_put = self.client.put(f'/api/tasks_sheets/{es_pk_1}/', attrs_edited)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.client.logout()

        self.client.login(username='test2', password='qwe111!!!')
        response_2 = self.client.post(f'/api/tasks_sheets/', self.task_sheet_attrs_exam_pk_user_2)
        es_pk_2 = response_2.data['id']

        attrs_edited_2 = dict(
            question='Changed question 2',
            exam_sheet=self.examsheet_2.pk,
            creator=self.user_2,
            score=25,
            answer='25'
        )
        response_put_403 = self.client.put(f'/api/tasks_sheets/{es_pk_1}/', attrs_edited_2)
        response_put_200 = self.client.put(f'/api/tasks_sheets/{es_pk_2}/', attrs_edited_2)
        self.assertEqual(response_put_403.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_put_200.status_code, status.HTTP_200_OK)
