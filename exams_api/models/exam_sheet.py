from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from dry_rest_permissions.generics import authenticated_users, allow_staff_or_superuser

from core.models.abstract_models import TimeStampedModel

User = get_user_model()


class ExamSheet(TimeStampedModel):
    class Meta:
        unique_together = ('creator', 'title',)

    title = models.CharField(max_length=256,
                             db_index=True,
                             )

    creator = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='examsheets'
                                )

    max_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    marks_range = models.ForeignKey('exams_api.MarksRange',
                                    on_delete=models.PROTECT,
                                    related_name='examsheets',
                                    null=True,
                                    )

    def __str__(self):
        return f'ExamSheet: {self.title}'

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
