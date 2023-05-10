from .models import *
from rest_framework.serializers import ModelSerializer

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields='__all__'

class CourseSerializer(ModelSerializer):
    class Meta:
        subject =SubjectSerializer()
        model= Course
        
