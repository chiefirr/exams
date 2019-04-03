from rest_framework.routers import DefaultRouter

from . import views

app_name = 'exams_api'

router = DefaultRouter()

router.register(r'exams', views.ExamViewSet)
router.register(r'exams_sheets', views.ExamSheetViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'tasks_sheets', views.TaskSheetViewSet)

urlpatterns = []
urlpatterns += router.urls
