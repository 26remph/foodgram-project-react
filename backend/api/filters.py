import django_filters as filters
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import StrIndex
from recipes.models import Ingredient


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

