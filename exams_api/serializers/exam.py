from django.db.models import Sum
from rest_framework import serializers

from exams_api.models import Exam


class ExamBaseSerializer(serializers.ModelSerializer):
    """Base exam serializer"""
    default_error_messages = {
        "empty_exam": "Ooops! This exam has no tasks! Try another one!",
        "lack_of_score": "Sorry, you can't start this exam - its max score is not reached yet."
                         " Ask the author: '{author}' to add more questions. Missing: {missing} points.",
    }

    score = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ('id', 'user', 'exam_sheet', 'score', 'progress', 'final_grade')
        read_only_fields = ('id', 'created', 'score', 'progress', 'user', 'final_grade')

    def get_exam_sheet(self, obj):
        from . import ExamSheetBaseSerializer
        return ExamSheetBaseSerializer(obj.exam_sheet).data

    def get_score(self, obj):
        return f'{obj.score}%'

    def validate(self, attrs):
        taken_score = attrs['exam_sheet'].task_sheets.all().aggregate(Sum('score'))
        if not taken_score['score__sum']:
            self.fail("empty_exam")
        elif taken_score['score__sum'] < attrs['exam_sheet'].max_score:
            self.fail("lack_of_score", author=attrs['exam_sheet'].creator,
                      missing=attrs['exam_sheet'].max_score - taken_score['score__sum'])
        return attrs
