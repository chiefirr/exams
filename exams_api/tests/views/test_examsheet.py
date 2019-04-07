from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

from exams_api.models import ExamSheet

User = get_user_model()


class TestExamSheetViewSet(APITestCase):
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

    def test_retrieve_examsheet_object_anon_user(self):
        examsheet = ExamSheet.objects.create(**self.exam_attrs)
        response_retrieve = self.client.get(f'/api/exams_sheets/{examsheet.pk}/')
        self.assertEqual(response_retrieve.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_examsheet_object_anon_user(self):
        examsheet_count = ExamSheet.objects.all().count()
        response_post = self.client.post(f'/api/exams_sheets/', self.exam_attrs)

        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ExamSheet.objects.all().count(), examsheet_count)

    def test_retrieve_examsheet_object_loggedin_user(self):
        self.client.login(username='test0', password='qwe111!!!')

        examsheet = ExamSheet.objects.create(**self.exam_attrs)
        response_retrieve = self.client.get(f'/api/exams_sheets/{examsheet.pk}/')
        response_retrieve_404 = self.client.get(f'/api/exams_sheets/{examsheet.pk + 1}/')
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve_404.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_examsheet_object(self):
        self.client.login(username='test0', password='qwe111!!!')

        examsheet_count = ExamSheet.objects.all().count()
        response_post = self.client.post(f'/api/exams_sheets/', self.exam_attrs)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamSheet.objects.all().count(), examsheet_count + 1)

    def test_perform_create_examsheet_duplicate(self):
        self.client.login(username='test0', password='qwe111!!!')
        self.client.post(f'/api/exams_sheets/', self.exam_attrs)

        response = self.client.post(f'/api/exams_sheets/', self.exam_attrs)
        self.assertEqual(response.data["error"].__str__(),
                         "You have already created an Exam Sheet with this title. Try another one.")

    def test_examsheet_user_permissions(self):
        self.client.login(username='test0', password='qwe111!!!')
        response = self.client.post(f'/api/exams_sheets/', self.exam_attrs)
        es_pk_1 = response.data['id']
        exam_sheet_1 = ExamSheet.objects.get(pk=es_pk_1)
        self.assertTrue(self.user.has_perm('exams_api.change_examsheet', exam_sheet_1))
        self.assertTrue(self.user.has_perm('exams_api.delete_examsheet', exam_sheet_1))

        attrs_edited = {'title': 'Changed test exam title'}
        response_put = self.client.put(f'/api/exams_sheets/{es_pk_1}/', attrs_edited)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.client.logout()

        self.client.login(username='test2', password='qwe111!!!')
        response = self.client.post(f'/api/exams_sheets/', self.exam_attrs_2)
        es_pk_2 = response.data['id']
        exam_sheet_2 = ExamSheet.objects.get(pk=es_pk_2)
        self.assertFalse(self.user_2.has_perm('exams_api.change_examsheet', exam_sheet_1))
        self.assertFalse(self.user_2.has_perm('exams_api.delete_examsheet', exam_sheet_1))
        self.assertTrue(self.user_2.has_perm('exams_api.change_examsheet', exam_sheet_2))
        self.assertTrue(self.user_2.has_perm('exams_api.delete_examsheet', exam_sheet_2))

        # attrs_edited_2 = {'title': 'Changed test exam title 2'}
        # response_put_403 = self.client.put(f'/api/exams_sheets/{es_pk_1}/', attrs_edited_2)
        # response_put_200 = self.client.put(f'/api/exams_sheets/{es_pk_2}/', attrs_edited_2)
        # self.assertEqual(response_put_403.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response_put_200.status_code, status.HTTP_200_OK)
