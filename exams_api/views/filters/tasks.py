from django_filters.rest_framework import FilterSet

from exams_api.models import Task


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {'score': ['exact', 'gte', 'lte'],
                  'user': ['exact'],
                  }
