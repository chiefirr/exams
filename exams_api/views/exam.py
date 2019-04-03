from core.views import MultiSerializerViewSet
from exams_api.models import Exam
from exams_api.serializers import ExamBaseSerializer


class ExamViewSet(MultiSerializerViewSet):
    queryset = Exam.objects.all()

    serializers = {'default': ExamBaseSerializer,
                   }

    # filter_backends = (DjangoFilterBackend, OrderingFilter)