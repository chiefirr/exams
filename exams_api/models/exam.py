from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from core.models.abstract_models import TimeStampedModel
from exams_api.helpers.models_helpers import check_final_grade
from exams_api.models.task import Task
from exams_api.models.task_sheet import TaskSheet

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
        all_tasks_results = Task.objects.select_related('task_sheet') \
            .filter(user=self.user, task_sheet__exam_sheet=self.exam_sheet) \
            .aggregate(Sum('score'))
        if all_tasks_results["score__sum"]:
            return round(all_tasks_results["score__sum"] / self.exam_sheet.max_score * 100, 2)
        else:
            return 0

    @property
    def progress(self):
        all_exam_tasks, finished_tasks = self._finished_and_all_tasks()
        return f'{finished_tasks}/{all_exam_tasks}'

    @property
    def final_grade(self):
        MESSAGES = {
            "not_defined": "Marks range is not defined for this Exam Sheet.",
            "not_completed_tasks": "Complete all tasks at this Exam Sheet to see your final grade.",
        }

        if not self.exam_sheet.marks_range:
            return MESSAGES["not_defined"]

        all_exam_tasks, finished_tasks = self._finished_and_all_tasks()

        if finished_tasks != all_exam_tasks:
            return MESSAGES["not_completed_tasks"]
        else:
            mark_range = self.exam_sheet.marks_range
            mark_rel = finished_tasks / all_exam_tasks
            return check_final_grade(mark_range, mark_rel)

    def _finished_and_all_tasks(self):
        """
        Method returns amount of finished tasks for selected Exam sheet for selected user
        and amount of all available tasks for that Exam sheet
        :return:
        """
        finished_tasks = Task.objects.select_related('task_sheet') \
            .filter(user=self.user, task_sheet__exam_sheet=self.exam_sheet).count()
        all_exam_tasks = TaskSheet.objects.filter(exam_sheet=self.exam_sheet).count()
        return all_exam_tasks, finished_tasks
