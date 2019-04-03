from rest_framework import serializers

from exams_api.models import Task


class TaskBaseSerializer(serializers.ModelSerializer):
    """Base task serializer"""
    class Meta:
        model = Task
        fields = ('id', 'user', 'task_sheet', 'answer', )

        read_only_fields = ('id', 'created', )
