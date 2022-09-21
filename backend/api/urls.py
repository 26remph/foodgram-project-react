from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
