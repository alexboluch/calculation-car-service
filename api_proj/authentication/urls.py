from .views import RegisterView
from django.urls import path, include, re_path        
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.conf.urls import url


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




# urlpatterns = [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('register/', RegisterView.as_view(), name='auth_register'),
# ]

urlpatterns = [
    # url(r'', include('djoser.urls')),
    # url(r'', include('djoser.urls.jwt')),
    path('auth/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/registration/', RegisterView.as_view(), name='auth_register'),
]



