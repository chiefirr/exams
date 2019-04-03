from rest_framework import serializers

from exams_api.models import Task


class TaskBaseSerializer(serializers.ModelSerializer):
    """Base task serializer"""
    right_answer = serializers.CharField(source='task_sheet.answer', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'task_sheet', 'answer', 'right_answer', )

        read_only_fields = ('id', 'created',)
