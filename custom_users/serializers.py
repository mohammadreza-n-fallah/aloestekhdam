from rest_framework import serializers
from .models import CustomUser




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ['user_type']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = [
                    'id' ,
                    'user_type' ,
                    'password' , 
                    'username' , 
                    'last_login' , 
                    'balance' ,
                    'email' ,
                    'is_superuser' ,
                    'is_staff',
                    'groups',
                    'phone_number_verfiy',
                    'phone_number',
                    'user_permissions',
                    ]