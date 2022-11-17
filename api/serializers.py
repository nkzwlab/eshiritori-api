from rest_framework import serializers
from .models import TestData, Histories

class TestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = '__all__'

class ImgWithStartCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        fields = (
            'id',
            'word',
            'img',
        )