from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MarksRange(models.Model):
    very_bad = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    bad = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    moderate = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    good = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    very_good = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'MarksRange: {self.pk}'
