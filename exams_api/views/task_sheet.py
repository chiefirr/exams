from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import assign_perm
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.views import MultiSerializerViewSet
from exams_api.models import TaskSheet
from exams_api.serializers import TaskSheetBaseSerializer
from exams_api.views.filters import TaskSheetsFilter


class TaskSheetViewSet(MultiSerializerViewSet):
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
        assign_perm('exams_api.change_examsheet', self.request.user)
        assign_perm('exams_api.delete_examsheet', self.request.user)
        serializer.save(creator=self.request.user)
