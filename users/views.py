from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
