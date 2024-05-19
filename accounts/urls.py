from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, RegisterUserView, UserView, AllUsersView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', AllUsersView.as_view()),
    path('user/', UserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
