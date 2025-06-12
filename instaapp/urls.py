# instagram_app/urls.py

from django.urls import path
from .views import InstagramUserAPIView,CreateUserFromInstagramAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('instagram/get-instagram-user/', InstagramUserAPIView.as_view(), name='instagram-get-user'),
    path('instagram/signup-user/', CreateUserFromInstagramAPIView.as_view(), name='signup-user'),
    path('instagram/signin-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Sign In
    path('instagram/signin-user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Refresh
]
