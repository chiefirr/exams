from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from core.views import MultiSerializerViewSet
from exams_api.exceptions import ExamsAPIError
from exams_api.models import Task
from exams_api.serializers import TaskBaseSerializer
from exams_api.views.filters import TaskFilter


class TaskViewSet(MultiSerializerViewSet):
    """
    Viewset to solve a concrete task sheet, post answer and get a result score for that answer.
    """
    http_method_names = ['get', 'post']

    queryset = Task.objects.all()

    serializers = {'default': TaskBaseSerializer,
                   }

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_class = TaskFilter
    ordering_fields = ('score', 'created')

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ExamsAPIError({'error': "You have already answered this question."})
