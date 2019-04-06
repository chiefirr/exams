from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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

