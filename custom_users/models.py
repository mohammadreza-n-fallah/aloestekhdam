from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin
from django.contrib.auth.hashers import make_password
from aloestekhdam.tokens import generate_tokens
from json import load


class CustomUserManager(BaseUserManager):

    def normalize_username(self, username):
        return username.lower()
    
    def create_user(self, username, password=None, **extra_fields):
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):

        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)





class CustomUser(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(max_length=250 , unique=True)
    password = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=100 , blank=True)
    has_company = models.BooleanField(default=False)
    organization_size = models.CharField(max_length=250 , blank=True)
    company_name = models.CharField(max_length=255 , blank=True)
    type_of_activity = models.CharField(max_length=250 , blank=True)
    established_year = models.CharField(max_length=250 , blank=True)
    ownership = models.CharField(max_length=250 , blank=True)
    phone_number = models.CharField(max_length=11 , unique=True)
    phone_number_verfiy = models.BooleanField(default=False)
    user_type = models.CharField(max_length=250)
    token = models.TextField(blank=True , null=True)


    def save_user(username , password , phone_number , email , user_type , method):
        errors = dict()
        number_file = open('validated_phones.json' , 'rb')
        number_list = load(number_file)

        if len(username) <= 6:
            errors['username'] = 'username_length_must_be_bigger_than_6'
        if len(password) <= 6:
            errors['password'] = 'password_length_must_be_bigger_than_6'
        if len(phone_number) < 11:
            errors['number'] = 'phone_number_length_must_be_bigger_than_11'
        if phone_number[:4:] not in number_list['numbers']:
            errors['number'] = 'number_is_not_valid'
        if len(errors) == 0:
            instance = CustomUser.objects.create(
            username = username,
            password = make_password(password),
            phone_number = phone_number,
            email = email,
            user_type = user_type,
            )
            generate_tokens(instance)
            if method == 'karjo':
                instance.has_company = False
                instance.save()
            elif method == 'karfarma':
                instance.has_company = True
                instance.save()
            else:
                return ({'error' : 'method_not_allowed'})
            return {'success':username}
        else:
            return errors


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()


