from django_filters.rest_framework import FilterSet

from exams_api.models import ExamSheet


class ExamSheetsFilter(FilterSet):
    class Meta:
        model = ExamSheet
        fields = {'creator': ['exact'],
                  'max_score': ['exact', 'gte', 'lte'],
                  }