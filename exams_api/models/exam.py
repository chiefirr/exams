from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from core.models.abstract_models import TimeStampedModel
from exams_api.models.task import Task

User = get_user_model()


class Exam(TimeStampedModel):
    class Meta:
        unique_together = ('user', 'exam_sheet',)

    user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='exams',
                                )

    exam_sheet = models.ForeignKey('exams_api.ExamSheet',
                                   on_delete=models.CASCADE,
                                   related_name='exams',
                                   )


    def __str__(self):
        return f'ExamSheet: {self.exam_sheet} for user {self.user}'



    @property
    def score(self):
        all_tasks_results = Task.objects.filter(user=self.user, task_sheet__exam_sheet=self.exam_sheet).aggregate(Sum('score'))
        return all_tasks_results["score__sum"]/self.exam_sheet.max_score*100