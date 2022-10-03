from django.db.models import Exists, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Follow, Ingredient, Recipe, Tag, User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDeleteMixinSet, CreateListDeleteMixinSet
from .pagination import RecipePagination
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeListRetrieveSerializer, TagSerializer)


# class FavoriteViewSet(CreateDeleteMixinSet):
class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get('id'))
        )

    def get_object(self):
        _id = self.kwargs.get('id')
        kwargs = {
            'user': self.request.user,
            'recipe': get_object_or_404(Recipe, id=_id),
        }
        instance = get_object_or_404(Favorite, kwargs)
        return instance

    def perform_destroy(self, instance):
        user = self.request.user
        pass


class FollowViewSet(CreateListDeleteMixinSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateUpdateSerializer
    permission_classes = (AllowAny,)
    # filter_backends = (filters.SearchFilter,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    # filterset_fields = ('tags__slug', 'author__id', )
    # search_fields = ('name',)
    # search_fields = ('$following__username', )
    # lookup_field = 'slug'
    pagination_class = RecipePagination
    # ordering = ('following__username', )

    # def get_queryset(self):
    #     user = self.request.user
    #     qs = Recipe.objects.all()
    #     qs.annotate(is_favoreted=Exists(user.recipe.favorites))
        # qs.annotate(is_favoreted=user.recipe.favorites.exist())
        # return qs
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListRetrieveSerializer

        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




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
