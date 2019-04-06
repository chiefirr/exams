from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

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
                                             )  # TODO - validate 0<score

    answer = models.TextField()

    # answer_type = models.ForeignKey(ContentType,
    #                                 on_delete=models.CASCADE,
    #                                 )
    #
    # object_id = models.PositiveIntegerField()
    #
    # content_object = GenericForeignKey()

    def __str__(self):
        return f"Task {self.pk}: to Exam Sheet '{self.exam_sheet}' - Question: '{self.question}'"
