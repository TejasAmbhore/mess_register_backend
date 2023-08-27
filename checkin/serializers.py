from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CheckInSerializer(serializers.ModelSerializer):
    foodChoice = serializers.SerializerMethodField()

    class Meta:
        model = CheckIn
        fields = ['id', 'rollNo', 'name', 'date', 'slot', 'food_type', 'foodChoice']

    def get_foodChoice(self, obj):
        return obj.user.foodChoice

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()