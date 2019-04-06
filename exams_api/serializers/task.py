from rest_framework import serializers

from exams_api.models import Task, Exam


class TaskBaseSerializer(serializers.ModelSerializer):
    """Base task serializer"""
    default_error_messages = {
        "cant_start_task": "You are did not created an Exam which contains this Task Sheet. You can't answer this Task Sheet yet.",
    }

    right_answer = serializers.CharField(source='task_sheet.answer', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'task_sheet', 'answer', 'right_answer',)
        read_only_fields = ('id', 'created', 'user',)

    def save(self, **kwargs):
        user = self.context['request'].user
        exam_sheet = self.context['request'].data.get('exam_sheet')
        exam = Exam.objects.filter(user=user, exam_sheet=exam_sheet)
        if not exam.exists():
            self.fail("cant_start_task")
        super().save(user=user)
