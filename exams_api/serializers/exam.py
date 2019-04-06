from rest_framework import serializers

from exams_api.models import Exam, ExamSheet


class ExamBaseSerializer(serializers.ModelSerializer):
    """Base exam serializer"""
    score = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = ('id', 'user', 'exam_sheet', 'score', 'progress',)
        read_only_fields = ('id', 'created', 'score', 'progress', 'user',)


    def get_exam_sheet(self, obj):
        from . import ExamSheetBaseSerializer
        return ExamSheetBaseSerializer(obj.exam_sheet).data

    def get_score(self, obj):
        return f'{obj.score}%'
