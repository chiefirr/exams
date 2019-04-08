from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.views import MultiSerializerViewSet
from exams_api.exceptions import ExamsAPIError
from exams_api.models import ExamSheet
from exams_api.serializers import ExamSheetBaseSerializer
from exams_api.views.filters import ExamSheetsFilter

User = get_user_model()


class ExamSheetViewSet(MultiSerializerViewSet):
    """
    Viewset to create exam sheet, which will be next available to add task sheets to it
    and to users to pass it and get a final grade.
    """
    permission_classes = (DRYPermissions,)
    queryset = ExamSheet.objects.select_related('creator').all()

    serializers = {'default': ExamSheetBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ExamSheetsFilter

    ordering_fields = ('max_score',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            serializer.save(creator=self.request.user)
        except IntegrityError:
            raise ExamsAPIError({'error': "You have already created an Exam Sheet with this title. Try another one."})
