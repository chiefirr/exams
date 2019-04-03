from rest_framework.routers import DefaultRouter

from . import views

app_name = 'core'
router = DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = []
urlpatterns += router.urls
