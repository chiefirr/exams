from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import assign_perm
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.views import MultiSerializerViewSet
from exams_api.exceptions import ExamsAPIError
from exams_api.models import TaskSheet
from exams_api.serializers import TaskSheetBaseSerializer
from exams_api.views.filters import TaskSheetsFilter


class TaskSheetViewSet(MultiSerializerViewSet):
    """
    Viewset for Task Sheet, which is a question to be solved.
    """
    queryset = TaskSheet.objects.select_related('creator').all()

    serializers = {'default': TaskSheetBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TaskSheetsFilter
    ordering_fields = ('created', 'score', 'creator')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        assign_perm('exams_api.change_tasksheet', self.request.user, serializer.instance)
        assign_perm('exams_api.delete_tasksheet', self.request.user, serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            serializer.save(creator=self.request.user)
        except IntegrityError:
            raise ExamsAPIError({'error': "This question already exists in this Exam Sheet."})

    # def retrieve(self, request, *args, **kwargs):
    #     # TODO - delete this method
    #     instance = self.get_object()
    #     aaa = self.request.user.has_perm('exams_api.change_tasksheet', instance)
    #     print("aaa = ", aaa)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
