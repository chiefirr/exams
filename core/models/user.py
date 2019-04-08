from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username}'
