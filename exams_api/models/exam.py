from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from core.models.abstract_models import TimeStampedModel
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
        finished_tasks = Task.objects.select_related('task_sheet') \
            .filter(user=self.user, task_sheet__exam_sheet=self.exam_sheet).count()

        all_exam_tasks = TaskSheet.objects.filter(exam_sheet=self.exam_sheet).count()
        return f'{finished_tasks}/{all_exam_tasks}'

    @property
    def final_grade(self):
        if not self.exam_sheet.marks_range:
            return "Marks range is not defined for this Exam Sheet."
        finished_tasks = Task.objects.select_related('task_sheet') \
            .filter(user=self.user, task_sheet__exam_sheet=self.exam_sheet).count()

        all_exam_tasks = TaskSheet.objects.filter(exam_sheet=self.exam_sheet).count()

        if finished_tasks != all_exam_tasks:
            return "Complete all tasks at this Exam Sheet to see your final grade."
        else:
            mark_range = self.exam_sheet.marks_range
            mark_rel = finished_tasks / all_exam_tasks
            return self._check_final_grade(mark_range, mark_rel)

    def _check_final_grade(self, mark_range, mark_rel):
        if mark_rel <= mark_range.very_bad:
            return 'Non-Certification'
        elif mark_range.very_bad < mark_rel <= mark_range.bad:
            return 'Very bad'
        elif mark_range.bad < mark_rel <= mark_range.moderate:
            return 'Bad'
        elif mark_range.moderate < mark_rel <= mark_range.good:
            return 'Moderate'
        elif mark_range.good < mark_rel <= mark_range.very_good:
            return 'Good'
        else:
            return 'Very good'
