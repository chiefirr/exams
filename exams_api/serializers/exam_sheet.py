from rest_framework import serializers

from core.serializers import ShortUserSerializer
from exams_api.models import ExamSheet


class ExamSheetBaseSerializer(serializers.ModelSerializer):
    """Base exam sheet serializer"""
    task_sheets = serializers.SerializerMethodField()
    creator = ShortUserSerializer(read_only=True)

    class Meta:
        model = ExamSheet
        fields = ('id', 'title', 'creator', 'max_score', 'task_sheets',)
        read_only_fields = ('id', 'created', 'creator',)

    def get_task_sheets(self, obj):
        from . import TaskSheetBaseSerializer
        return TaskSheetBaseSerializer(obj.task_sheets, many=True, read_only=True).data
