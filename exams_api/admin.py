from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from exams_api.models import ExamSheet, TaskSheet, Exam, Task, MarksRange


class ExamSheetAdmin(GuardedModelAdmin):
    pass


class TaskSheetAdmin(GuardedModelAdmin):
    pass


class ExamAdmin(GuardedModelAdmin):
    pass


class TaskAdmin(GuardedModelAdmin):
    pass


class MarksRangeAdmin(GuardedModelAdmin):
    pass


admin.site.register(ExamSheet, ExamSheetAdmin)
admin.site.register(TaskSheet, TaskSheetAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(MarksRange, MarksRangeAdmin)
