from django.contrib.auth import get_user_model

from core.serializers import UserSerializer
from core.views import MultiSerializerViewSet

User = get_user_model()


class UserViewSet(MultiSerializerViewSet):
    queryset = User.objects.all()

    serializers = {
        'default': UserSerializer,
    }
