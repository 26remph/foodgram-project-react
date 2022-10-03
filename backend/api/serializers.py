import base64

from django.core.files.base import ContentFile
from django.db import transaction
from djoser import serializers as djoser_serializer
from djoser.conf import settings
from recipes.models import (Favorite, Follow, Ingredient, IngredientAmount,
                            Recipe, Tag, User)
from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404


class UserProfileSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        return False


class UserCreateSerializer(djoser_serializer.UserCreateSerializer):
    """Сериализация зарегистрированных пользователей"""

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username',
            'first_name', 'last_name',
            'password'
        )

    @staticmethod
    def get_user_name(email):
        nic = email.split('@')[0]
        domain = email.split('@')[1]
        domain = domain[:domain.find('.')]
        return '.'.join([nic, domain])

    def perform_create(self, validated_data):
        with transaction.atomic():

            if settings.LOGIN_FIELD == 'email':
                if validated_data.get('username'):
                    email: str = validated_data.get('email')
                    validated_data['username'] = self.get_user_name(email)

            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализация подписок."""
    id = serializers.IntegerField(source='recipe.id', required=False)
    name = serializers.CharField(source='recipe.name', required=False)
    image = serializers.CharField(source='recipe.image', required=False)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', required=False
    )

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time', )
        model = Favorite


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация подписок."""

    class Meta:
        fields = '__all__'
        model = Follow


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов."""

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов."""
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(required=False)
    measurement_unit = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        fields = '__all__'
        model = Ingredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


# class IngredientAmountSerializer(serializers.RelatedField):
# class IngredientAmountSerializer(serializers.Field):
class IngredientAmountSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='ingredient.name')
    id = serializers.IntegerField(source='ingredient.id')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount', )
        model = IngredientAmount


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    """Сериализация для получения рецептов."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserProfileSerializer()
    ingredients = IngredientAmountSerializer(
        many=True, source='ingredient_amounts'
    )

    class Meta:
        exclude = ('pub_date', )
        model = Recipe

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализация для создания и обновления рецептов."""

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='id'
    )
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        # fields = '__all__'
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name',
            'text', 'cooking_time',
        )

    @staticmethod
    def create_ingredient(recipe, ingredients):

        for order_dict in ingredients:
            amount = order_dict.get('amount')
            _id = order_dict.get('id')
            ingredient = get_object_or_404(Ingredient, pk=_id)

            IngredientAmount.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount,
            )

    def create(self, validated_data):

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe, status = Recipe.objects.get_or_create(**validated_data)
        recipe.tags.set(tags)

        with transaction.atomic():

            self.create_ingredient(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)

        tags = validated_data.pop('tags')
        instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients')

        with transaction.atomic():

            qs = instance.ingredient_amounts.all()
            qs.delete()

            self.create_ingredient(instance, ingredients)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
