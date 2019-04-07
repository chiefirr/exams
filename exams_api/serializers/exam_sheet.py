from rest_framework import serializers

from core.serializers import ShortUserSerializer
from exams_api.models import ExamSheet


class ExamSheetBaseSerializer(serializers.ModelSerializer):
    """Base exam sheet serializer"""
    default_error_messages = {
        "cant_assign_range": "Bad marks range for this Exam Sheet. Too high 'very good' mark score.",
    }

    task_sheets = serializers.SerializerMethodField()
    creator = ShortUserSerializer(read_only=True)

    class Meta:
        model = ExamSheet
        fields = ('id', 'title', 'creator', 'max_score', 'task_sheets', 'marks_range',)
        read_only_fields = ('id', 'created', 'creator',)

    def validate_marks_range(self, marks_range):
        if marks_range and marks_range.very_good > int(self.initial_data['max_score']):
            self.fail("cant_assign_range")

    def get_task_sheets(self, obj):
        from . import TaskSheetBaseSerializer
        return TaskSheetBaseSerializer(obj.task_sheets, many=True, read_only=True).data
