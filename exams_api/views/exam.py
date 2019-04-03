from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from core.views import MultiSerializerViewSet
from exams_api.models import Exam
from exams_api.serializers import ExamBaseSerializer
from exams_api.views.filters import ExamFilter


class ExamViewSet(MultiSerializerViewSet):
    queryset = Exam.objects.all()

    serializers = {'default': ExamBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ExamFilter

    ordering_fields = ('created',)