from rest_framework import serializers
from .models import CustomUser
from jobads.models import CV


class UserSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        exclude = ['user_type']

    class s_data(serializers.ModelSerializer):
        class Meta:
            model = CV
            fields = '__all__'

    def get_sent_cv(self, obj):
        data = obj.user_sent_cv.filter()
        return self.s_data(data, many=True).data


class CompanySerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        exclude = [
            'id',
            'user_type',
            'password',
            'username',
            'last_login',
            'balance',
            'email',
            'is_superuser',
            'is_staff',
            'groups',
            'phone_number_verfiy',
            'phone_number',
            'user_permissions',
        ]
