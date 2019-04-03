from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.compat import MinValueValidator

from core.models.abstract_models import TimeStampedModel

User = get_user_model()


class Task(TimeStampedModel):
    class Meta:
        unique_together = ('user', 'task_sheet', )

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='tasks',
                             )

    task_sheet = models.ForeignKey('exams_api.TaskSheet',
                                   on_delete=models.CASCADE,
                                   related_name='tasks',
                                   )

    answer = models.TextField()

    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],
                                             default=0,
                                             )

    def __str__(self):
        return f'Task {self.pk} finished by user {self.user}'


    def save(self, *args, **kwargs):
        if self.answer == self.task_sheet.answer:
            self.score = self.task_sheet.score
        else:
            self.score = 0
        super().save(*args, **kwargs)
