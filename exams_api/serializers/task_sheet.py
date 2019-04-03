from rest_framework import serializers

from exams_api.models import TaskSheet


class TaskSheetBaseSerializer(serializers.ModelSerializer):
    """Base task sheet serializer"""
    class Meta:
        model = TaskSheet
        fields = ('id', 'question', 'creator', 'exam_sheet', 'score', 'answer', )

        read_only_fields = ('id', 'created',)
