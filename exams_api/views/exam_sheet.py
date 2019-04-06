from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from core.views import MultiSerializerViewSet
from exams_api.models import ExamSheet
from exams_api.serializers import ExamSheetBaseSerializer
from exams_api.views.filters import ExamSheetsFilter


class ExamSheetViewSet(MultiSerializerViewSet):
    queryset = ExamSheet.objects.select_related('creator').all()

    serializers = {'default': ExamSheetBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ExamSheetsFilter

    ordering_fields = ('max_score',)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

