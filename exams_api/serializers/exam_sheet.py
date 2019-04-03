from rest_framework import serializers

from exams_api.models import ExamSheet



class ExamSheetBaseSerializer(serializers.ModelSerializer):
    """Base exam sheet serializer"""
    task_sheets = serializers.SerializerMethodField()

    class Meta:
        model = ExamSheet
        fields = ('id', 'title', 'creator', 'max_score', 'task_sheets', )

        read_only_fields = ('id', 'created',)

        # TODO - field creator writable only on POST and read_only on PUT

    def get_task_sheets(self, obj):
        from . import TaskSheetBaseSerializer
        return TaskSheetBaseSerializer(obj.task_sheets, many=True, read_only=True).data