from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register(r'films', FilmViewSet)
router.register(r'character', CharacterViewSet)
router.register(r'starships', StarshipViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("sync/", SyncView.as_view(), name="sync"),
]
