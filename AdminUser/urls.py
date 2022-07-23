from django.urls import path
from .views import MovieModelViewSetAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('movies', MovieModelViewSetAPIView)

urlpatterns = [
    * router.urls
]