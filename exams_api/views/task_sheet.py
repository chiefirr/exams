from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
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
    permission_classes = (DRYPermissions,)
    queryset = TaskSheet.objects.select_related('creator').all()

    serializers = {'default': TaskSheetBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TaskSheetsFilter
    ordering_fields = ('created', 'score', 'creator')

    def perform_create(self, serializer):
        try:
            serializer.save(creator=self.request.user)
        except IntegrityError:
            raise ExamsAPIError({'error': "This question already exists in this Exam Sheet."})
