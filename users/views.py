from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .serializers import UserSerializer,AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    