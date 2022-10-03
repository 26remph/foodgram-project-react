from django.db.models import Exists, F, FilteredRelation, OuterRef, Q
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Favorite, Follow, Ingredient, Recipe, Tag,
                            User)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDeleteMixinSet, CreateListDeleteMixinSet
from .pagination import FoodgramPagination
from .serializers import (CartSerializer, FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeListRetrieveSerializer, TagSerializer)


class CartViewSet(CreateDeleteMixinSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get('id'))
        )

    def get_object(self):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        instance = get_object_or_404(
            Cart,
            Q(user__id=self.request.user.id) & Q(recipe__id=recipe.id)
        )
        return instance


class FavoriteViewSet(CreateDeleteMixinSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe, id=self.kwargs.get('id'))
        )

    def get_object(self):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        instance = get_object_or_404(
            Favorite,
            Q(user__id=self.request.user.id) & Q(recipe__id=recipe.id)
        )
        return instance


class FollowViewSet(CreateListDeleteMixinSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (AllowAny, )
    pagination_class = FoodgramPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(ModelViewSet):
    # queryset = Recipe.objects.all()
    serializer_class = RecipeCreateUpdateSerializer
    permission_classes = (AllowAny,)
    # filter_backends = (filters.SearchFilter,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    # filterset_fields = ('tags__slug', 'author__id', )
    # search_fields = ('name',)
    # search_fields = ('$following__username', )
    # lookup_field = 'slug'
    pagination_class = FoodgramPagination
    # ordering = ('following__username', )

    def get_queryset(self):
        is_in_shopping_cart = Cart.objects.filter(
            user__id=self.request.user.id, recipe=OuterRef('id')
        )
        is_favorited = Favorite.objects.filter(
            user__id=self.request.user.id, recipe=OuterRef('id')
        )
        return (
            Recipe.objects.annotate(
                is_favorited=Exists(is_favorited),
                is_in_shopping_cart=Exists(is_in_shopping_cart)
            )
        )


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
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
