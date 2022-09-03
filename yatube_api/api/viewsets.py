from rest_framework import mixins, viewsets


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Custom ViewSet that performs list() and create() actions"""

    pass
