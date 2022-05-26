
from Utils import custome_mixin_class as custom_mixins
from rest_framework import viewsets

class ModelViewSet(custom_mixins.CreateModelMixin,
                   custom_mixins.RetrieveModelMixin,
                   custom_mixins.UpdateModelMixin,
                   custom_mixins.DestroyModelMixin,
                   custom_mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass