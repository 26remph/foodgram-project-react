from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser import serializers as djoser_serializer
from djoser.conf import settings
from recipes.models import Follow, Ingredient, Recipe, Tag, User
from rest_framework import serializers, validators


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация подписок."""

    class Meta:
        fields = '__all__'
        model = Follow

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


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов."""

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализация рецептов."""

    class Meta:
        fields = '__all__'
        model = Recipe
