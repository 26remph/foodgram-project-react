from pprint import pprint

import djqscsv
import recipes.models
from django.db.models import (Count, Exists, F, FilteredRelation, OuterRef, Q,
                              Subquery, Sum)
from django.db.models import Value as V
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Favorite, Follow, Ingredient,
                            IngredientAmount, Recipe, Tag, User)
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDeleteMixinSet, CreateListDeleteMixinSet
from .pagination import FoodgramPagination
from .serializers import (CartSerializer, FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeListRetrieveSerializer, TagSerializer)


class DownloadCartView(APIView):
    """Формирование и отправка списка покупок пользователю."""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = IngredientAmount.objects.filter(
            recipe__carts__user__id=self.request.user.id
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            check=V('▢'),
            ingredient=Concat(
                'ingredient__name',
                V('('), 'ingredient__measurement_unit', V(')')),
            amount=Sum('amount')
        ).order_by(
            'ingredient__name', 'ingredient__measurement_unit'
        )

        return (
            djqscsv.render_to_csv_response(
                qs.values('check', 'ingredient', 'amount'))
        )


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
    # queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (AllowAny,)
    pagination_class = FoodgramPagination

    def get_queryset(self):
        # recipes_limit
        user = User.objects.get(pk=4)
        # user = self.request.user.follow

        # subquery = Recipe.objects.filter(
        #     author__following__user=OuterRef('author_id')
        # ).order_by('author_id')
        # qs = Recipe.objects.filter(
        #     author__following__user=user
        # ).order_by('author_id')
        # subquery = Recipe.objects.filter(
        #     author__following__user=user, author_id=OuterRef('author_id')
        # ).order_by('author_id')

        # qs = (
        #     user.follower.annotate(
        #         recipes_count=Count('author__recipe'),
        #         is_subscribed=V(True)
        #     )
        # )

        # qs = (
        #     user.follower.annotate(
        #         recipes_count=Count('author__recipe'),
        #         is_subscribed=V(True)
        #     ).filter(author__recipe__name=subquery.values('name'))
        # )


        # qs = (
        #     user.follower.annotate(
        #         recipes=Subquery(subquery.values('image')[:10]),
        #         recipes_count=Count('author__recipe'),
        #         is_subscribed=V(True)
        #     )
        # )
        from itertools import chain

        qs = user.follower.annotate(
            recipes_count=Count('author__recipe'),
            is_subscribed=V(True)
        )

        subquery_1 = Recipe.objects.filter(
                author__following__user__id=4, author_id=3
            )
        print(subquery_1)
        subquery_2 = Recipe.objects.filter(
                author__following__user__id=4, author_id=7
            )
        print(subquery_2)
        match = subquery_1 | subquery_2
        print(subquery_1 | subquery_2)
        print(type(match), len(match))

        qs_init = Recipe.objects.none()
        my_list = []
        for row in qs:
            print(f'{row.id}, {row}, author_id: {row.author_id}, {row.author}')

            subquery = Recipe.objects.filter(
                author__following__user=user, author_id=row.author_id
            ).annotate(recipes_count=Count('author__recipe'))[:3]
            my_list.append(subquery)
            print(subquery)

        print(*my_list)

        return qs_init.union(*my_list)
        # return (
        #     user.follower.annotate(
        #         recipes=F('author__recipe'),
        #         recipes_count=Count('author__recipe'),
        #         is_subscribed=V(True)
        #     )
        # )

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, author=author)

    def get_object(self):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        instance = get_object_or_404(
            Follow,
            Q(user__id=self.request.user.id) & Q(author__id=author.id)
        )
        return instance


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
    permission_classes = (AllowAny,)
