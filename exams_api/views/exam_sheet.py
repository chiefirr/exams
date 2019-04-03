from core.views import MultiSerializerViewSet
from exams_api.models import ExamSheet
from exams_api.serializers import ExamSheetBaseSerializer


class ExamSheetViewSet(MultiSerializerViewSet):
    queryset = ExamSheet.objects.all()

    serializers = {'default': ExamSheetBaseSerializer,
                   }

    # filter_backends = (DjangoFilterBackend, OrderingFilter)
