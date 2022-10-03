
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users/subscriptions', FollowViewSet, basename='subscriptions')
# router.register(
#     r"recipes/(?P<id>[^/.]+)/favorite", FavoriteViewSet, basename='favorites'
# )
# v1_router.register(
#     r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
#     CommentViewSet,
#     basename='comment'
# )


urlpatterns = [
    path('', include(router.urls)),
    path(r'recipes/(?P<id>[^/.]+)/favorite/', FavoriteViewSet),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'', include('djoser.urls')),
]