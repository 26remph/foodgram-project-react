from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from .settings import MAX_LENGTH_CHAR_FIELD, MAX_LENGTH_COLOR_FIELD

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_CHAR_FIELD
    )
    color = models.CharField(
        max_length=MAX_LENGTH_COLOR_FIELD,
        null=True
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_CHAR_FIELD,
        unique=True,
        validators=[
            RegexValidator(regex='^[-a-zA-Z0-9_]+$')
        ]
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модуль для создания ингредиентов."""

    name = models.CharField(max_length=MAX_LENGTH_CHAR_FIELD)
    measurement_unit = models.CharField(max_length=MAX_LENGTH_CHAR_FIELD)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов"""
    tags = models.ManyToManyField('Tag', related_name='recipe')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='author'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipe',
        through='IngredientAmount'
    )

    pub_date = models.DateTimeField(
        'Publishing date',
        auto_now_add=True,
        db_index=True
    )
    name = models.CharField(max_length=MAX_LENGTH_CHAR_FIELD)
    image = models.ImageField(
        upload_to='recipe/images/',
        null=True,
        default=None
    )
    text = models.TextField(
        verbose_name='Description recipe',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'minimal time - 1 min')
        ]
    )

    class Meta:
        ordering = ('pub_date', )

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Вспомогательная модель для расчета количества ингредиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredient_amounts'
    )
    amount = models.PositiveIntegerField(
        default=None,
        validators=[
            MinValueValidator(1, 'minimal quantity - 1')
        ]
    )

    class Meta:
        ordering = ('ingredient', )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class Favorite(models.Model):
    """Модель для работы с избранными рецептами."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        indexes = [
            models.Index(fields=['user', 'recipe'], name='user_favor_recipe'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class Cart(models.Model):
    """Модель для работы со списком покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts'
    )

    class Meta:
        indexes = [
            models.Index(fields=['user', 'recipe'], name='user_cart_recipe'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            )
        ]


