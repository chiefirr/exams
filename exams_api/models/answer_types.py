from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class AnswerBool(models.Model):
    body = models.BooleanField()
    tasks = GenericRelation("exams_api.Task")


class AnswerSingleChoice(models.Model):
    choice = models.ForeignKey("exams_api.AnswerSingleChoiceOption",
                               on_delete=models.CASCADE,
                               related_name="choises")
    tasks = GenericRelation("exams_api.Task")


class AnswerFillIn(models.Model):
    body = models.TextField()
    tasks = GenericRelation("exams_api.Task")


class AnswerFree(models.Model):
    body = models.TextField()
    tasks = GenericRelation("exams_api.Task")


class AnswerSingleChoiceOption(models.Model):
    content = models.CharField(max_length=128)
