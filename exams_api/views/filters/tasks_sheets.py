from django_filters.rest_framework import FilterSet

from exams_api.models import TaskSheet


class TaskSheetsFilter(FilterSet):
    class Meta:
        model = TaskSheet
        fields = {'creator': ['exact'],
                  'score': ['exact', 'gte', 'lte'],
                  }
