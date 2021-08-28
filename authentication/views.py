from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from api import views
from api import backends
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = (backends.CsrfExemptSessionAuthentication,)

class UpdatePassView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, views.IsOwner]
    authentication_classes = [backends.CsrfExemptSessionAuthentication, JWTAuthentication]