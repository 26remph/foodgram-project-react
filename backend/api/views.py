from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    # filter_backends = (filters.SearchFilter,)
    # filter_backends = (DjangoFilterBackend,)
    # search_fields = ('name',)
    # search_fields = ('$following__username', )
    # lookup_field = 'slug'
    # pagination_class = LimitOffsetPagination
    # ordering = ('following__username', )
    # filter_backends = (DjangoFilterBackend, )
    # filterset_class = TitleFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """Представление для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
