from core.views import MultiSerializerViewSet
from exams_api.models import TaskSheet
from exams_api.serializers import TaskSheetBaseSerializer


class TaskSheetViewSet(MultiSerializerViewSet):
    queryset = TaskSheet.objects.select_related('creator').all()

    serializers = {'default': TaskSheetBaseSerializer,
                   }

    # filter_backends = (DjangoFilterBackend, OrderingFilter)
