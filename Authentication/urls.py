from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import UsersInfoModelViewSetAPIView, UserAddressModelViewSetAPIView

router = DefaultRouter(trailing_slash=False)

router.register('user_info', UsersInfoModelViewSetAPIView)
router.register('user_address', UserAddressModelViewSetAPIView)

urlpatterns = [
    * router.urls
]