from django.db.models import Sum
from rest_framework import serializers

from exams_api.models import TaskSheet, ExamSheet


class TaskSheetBaseSerializer(serializers.ModelSerializer):
    """Base task sheet serializer"""
    default_error_messages = {
        "bad_creator": "You are not creator of this Exam Sheet. You can't add Task Sheets here. Create your own Exam Sheet.",
        "too_big_score": "This score exceeds maximal allowed Exam Sheet score. Free score points left: {amount}",
    }

    class Meta:
        model = TaskSheet
        fields = ('id', 'question', 'creator', 'exam_sheet', 'score', 'answer',)

        read_only_fields = ('id', 'created', 'creator',)

    def validate_score(self, score):
        exam_sheet = ExamSheet.objects.prefetch_related('task_sheets') \
            .filter(pk=self.context['request'].data.get('exam_sheet')) \
            .annotate(taken_score=Sum('task_sheets__score'))

        taken_score = exam_sheet[0].taken_score
        max_score = exam_sheet[0].max_score
        if taken_score and score + taken_score > max_score:
            self.fail("too_big_score", amount=(max_score - taken_score))
        return score

    def save(self, **kwargs):
        user = self.context['request'].user
        exam_sheet = ExamSheet.objects.get(pk=self.context['request'].data.get('exam_sheet'))
        if user != exam_sheet.creator:
            self.fail("bad_creator")
        super().save(creator=user)
