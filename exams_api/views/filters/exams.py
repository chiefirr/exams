from django_filters.rest_framework import FilterSet

from exams_api.models import Exam


class ExamFilter(FilterSet):
    class Meta:
        model = Exam
        fields = {'user': ['exact'],
                  }
