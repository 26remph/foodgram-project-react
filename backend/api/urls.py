
from django.urls import include, path
from rest_framework.routers import DefaultRouter, Route, SimpleRouter

from .routers import ExtendedEndpointRouter
from .views import (CartViewSet, DownloadCartView, FavoriteViewSet,
                    FollowViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

ext_router = ExtendedEndpointRouter()
ext_router.register(
    r"recipes/(?P<id>[^/.]+)/shopping_cart", CartViewSet, basename='carts'
)
ext_router.register(
    r"recipes/(?P<id>[^/.]+)/favorite", FavoriteViewSet, basename='favorites'
)
ext_router.register(
    r'users/(?P<id>[^/.]+)/subscribe', FollowViewSet, basename='subscriptions'
)

urlpatterns = [
    path(r'recipes/download_shopping_cart/', DownloadCartView.as_view(),
         name='download_cart'),
    path('', include(ext_router.urls)),
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'', include('djoser.urls')),
]