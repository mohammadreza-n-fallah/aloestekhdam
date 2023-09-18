from rest_framework import serializers
from .models import CustomUser




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ['token' , 'user_type']