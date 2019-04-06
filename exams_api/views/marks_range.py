from core.views import MultiSerializerViewSet
from exams_api.models import MarksRange
from exams_api.serializers import MarksRangekBaseSerializer


class MarksRangeViewSet(MultiSerializerViewSet):
    http_method_names = ['get', 'post']
    queryset = MarksRange.objects.all()

    serializers = {'default': MarksRangekBaseSerializer,
                   }
