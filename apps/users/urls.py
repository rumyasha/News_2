from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    UserProfileAPIView,
    ChangePasswordAPIView,
    UserListAPIView,
    DeleteUserAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete-user'),
]