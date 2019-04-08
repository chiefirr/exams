from django.contrib.auth.models import AbstractUser
from guardian.shortcuts import assign_perm


class ExtendedUser(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username}'
