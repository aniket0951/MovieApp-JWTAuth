from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import TheterInformationModelViewSetAPIView

router = DefaultRouter(trailing_slash=False)

router.register('theter_info', TheterInformationModelViewSetAPIView)

urlpatterns = [
    * router.urls
]