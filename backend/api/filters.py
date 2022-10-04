import django_filters as filters
from django.db.models import F, Q
from django.db.models import Value as V
from django.db.models.functions import StrIndex
from recipes.models import Ingredient, Recipe

ENUM = (0, 1)


class IngredientFilter(filters.FilterSet):
    """Фильтр для ингредиентов.

    Двойная фильтрация ингредиентов по вхождению в начало названия и вхождению
    в произвольном месте. Сортировка от первых ко вторым.
    """

    name = filters.CharFilter(method='multiple_filter')

    class Meta:
        model = Ingredient
        fields = ('name', )

    @staticmethod
    def multiple_filter(queryset, name, value):

        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        ).order_by(StrIndex(name, V(value)).asc())


class RecipeFilter(filters.FilterSet):
    """Фильтры для рецептов. """

    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.NumberFilter(
        field_name='is_favorited', method='boolean_filter'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='is_in_shopping_cart', method='boolean_filter'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', )

    def boolean_filter(self, queryset, name, value):
        return (
            queryset.filter(**{name: value})
            if value in ENUM else queryset
        )

