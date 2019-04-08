from django.contrib.auth import get_user_model
from django.db import models
from dry_rest_permissions.generics import authenticated_users
from rest_framework.compat import MinValueValidator

from core.models.abstract_models import TimeStampedModel

User = get_user_model()


class Task(TimeStampedModel):
    class Meta:
        unique_together = ('user', 'task_sheet',)

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

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return False

    def has_object_update_permission(self, request):
        return False
