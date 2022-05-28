from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import TheterInformationModelViewSetAPIView, ScreenModelViewSetAPIView

router = DefaultRouter(trailing_slash=False)

router.register('theter_info', TheterInformationModelViewSetAPIView)
router.register('screens_info', ScreenModelViewSetAPIView)

urlpatterns = [
    * router.urls
]