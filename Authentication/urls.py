from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import UsersInfoModelViewSetAPIView, VerifyUsersModelViewSetAPIView

router = DefaultRouter(trailing_slash=False)

router.register('user_info', UsersInfoModelViewSetAPIView)
router.register('verify_user', VerifyUsersModelViewSetAPIView)

urlpatterns = [
    * router.urls
]