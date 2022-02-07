from rest_framework.serializers import ModelSerializer
from .models import *


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'   # All fields
        # fields = ['file', 'name']
        # exclude = ['id']
