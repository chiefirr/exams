from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from dry_rest_permissions.generics import allow_staff_or_superuser, authenticated_users

from core.models.abstract_models import TimeStampedModel

User = get_user_model()


class TaskSheet(TimeStampedModel):
    class Meta:
        unique_together = ('creator', 'question', 'exam_sheet')

    question = models.CharField(max_length=512,
                                db_index=True,
                                )

    exam_sheet = models.ForeignKey('exams_api.ExamSheet',
                                   on_delete=models.CASCADE,
                                   related_name='task_sheets'
                                   )

    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='task_sheets'
                                )

    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],
                                             default=0,
                                             )

    answer = models.TextField()

    def __str__(self):
        return f"Task {self.pk}: to Exam Sheet '{self.exam_sheet}' - Question: '{self.question}'"

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.creator

    def has_object_update_permission(self, request):
        return request.user == self.creator
