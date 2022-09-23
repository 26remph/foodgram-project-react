from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# app_name = 'api'

# router = DefaultRouter()
# router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path(r'auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    # path('', include(router.urls)),
]