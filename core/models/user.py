from django.contrib.auth.models import AbstractUser
from guardian.shortcuts import assign_perm


class ExtendedUser(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username} {(self.pk)}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        assign_perm('exams_api.add_examsheet', self)
        assign_perm('exams_api.add_exam', self)
        assign_perm('exams_api.add_tasksheet', self)
        assign_perm('exams_api.add_task', self)
