from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class CreateDeleteMixinSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """Миксин для вьюсетов. Поддерживает создание и удаление."""
    permission_classes = (IsAuthenticated,)


class CreateListDeleteMixinSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        GenericViewSet):
    """
    Миксин для вюсетов: Поддерживает вывод списком, создание, удаление.
    """
    permission_classes = (IsAuthenticated,)
