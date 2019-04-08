from django.contrib import admin

from exams_api.models import ExamSheet, TaskSheet, Exam, Task, MarksRange

admin.site.register(ExamSheet)
admin.site.register(TaskSheet)
admin.site.register(Exam)
admin.site.register(Task)
admin.site.register(MarksRange)
