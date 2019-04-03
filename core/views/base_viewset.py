from rest_framework import viewsets


class MultiSerializerViewSet(viewsets.ModelViewSet):
    """
    Viewset with custom get_serializer_class. Allows to have multiple serializers for each viewset.
    Default serializer has to be specified and is returned by default.
    """
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
