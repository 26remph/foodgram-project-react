import django_filters as filters
from django.db.models import F, Q
from django.db.models import Value as V
from django.db.models.functions import StrIndex
from recipes.models import Ingredient, Recipe, Tag

ENUM = (
    (0, 0),
    (1, 1),
)

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

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    author = filters.NumberFilter(field_name='author__id')

    is_favorited = filters.TypedChoiceFilter(
        field_name='is_favorited', choices=ENUM
    )
    is_in_shopping_cart = filters.TypedChoiceFilter(
        field_name='is_in_shopping_cart', choices=ENUM
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', )

