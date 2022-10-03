from django.contrib import admin
from django.contrib.admin import register
from recipes.models import (Cart, Favorite, Follow, Ingredient,
                            IngredientAmount, Recipe, Tag, User)


@register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Административная модель для работы со списком покупок."""
    list_display = ('user', 'recipe', )
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-empty-'


@register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная модель для избранных рецептов."""
    list_display = ('user', 'recipe', )
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-empty-'


@register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Административная модель для подписок на авторов."""

    list_display = ('user', 'author', )
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author')
    empty_value_display = '-empty-'


@register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Административная модель для вспомогательной таблицы ингредиентов."""
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', )
    empty_value_display = '-empty-'

@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная модель для ингредиентов."""

    list_display = ('name', 'measurement_unit', )
    search_fields = ('name',)
    list_filter = ('measurement_unit', )
    empty_value_display = '-empty-'


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная модель для тегов."""
    list_display = ('id', 'name', 'color', 'slug', )
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug', 'color')
    empty_value_display = '-empty-'


@register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    """Административная модель для рецептов."""
    list_display = (
        'name', 'author', 'pub_date', 'cooking_time', 'cnt_favorites'
    )
    search_fields = ('name', )
    list_filter = ('tags', 'author', 'name')
    empty_value_display = '-empty-'

    def cnt_favorites(self, obj):
        return obj.favorites.count()


class UserAdmin(admin.ModelAdmin):
    """Административная модель пользователя."""
    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'is_staff', 'is_active',
        'last_login', 'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
    empty_value_display = '-empty-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
