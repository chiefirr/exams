from core.views import MultiSerializerViewSet
from exams_api.models import Task
from exams_api.serializers import TaskBaseSerializer


class TaskViewSet(MultiSerializerViewSet):
    queryset = Task.objects.all()

    serializers = {'default': TaskBaseSerializer,
                   }

    # filter_backends = (DjangoFilterBackend, OrderingFilter)
