from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from json import load
from datetime import timedelta, timezone


def cv_upload_to(instance, filename):
    return f'users/user_cvs/{instance}/{filename}'


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)


def image_upload_to(instance, filename):
    return f'users/user_images/{instance}/{filename}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True, blank=True, null=True)
    password = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250, blank=True)
    image = models.FileField(upload_to=image_upload_to, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, blank=True)
    balance = models.CharField(max_length=500, default=0, blank=True)
    user_cv = models.FileField(upload_to=cv_upload_to, blank=True)
    has_company = models.BooleanField(default=False)
    industry = models.CharField(max_length=250, default='')
    state = models.ForeignKey('custom_users.State', blank=True, null=True, on_delete=models.CASCADE)
    phone_number_2 = models.CharField(max_length=250, default='')
    website = models.CharField(max_length=250, blank=True)
    company_telephone = models.CharField(max_length=250, default='')
    company_telephone_2 = models.CharField(max_length=250, default='')
    organization_side = models.CharField(max_length=250, default='')
    service_and_products = models.CharField(max_length=250, default='')
    description_of_company = models.TextField(default='')
    organization_size = models.CharField(max_length=250, default='')
    company_name = models.CharField(max_length=255, default='')
    type_of_activity = models.CharField(max_length=250, default='')
    established_year = models.CharField(max_length=250, default='')
    brand = models.CharField(max_length=250, default='')
    ownership = models.CharField(max_length=250, default='')
    phone_number = models.CharField(max_length=11, unique=True)
    phone_number_verfiy = models.BooleanField(default=False)
    user_type = models.CharField(max_length=250, default='casual')

    def save_user(username, password, phone_number, user_type, method):
        errors = dict()
        number_file = open('validated_phones.json', 'rb')
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
                username=username,
                password=make_password(password),
                phone_number=phone_number,
                user_type=user_type,
            )
            if method == 'karjo':
                instance.has_company = False
                instance.save()
            elif method == 'karfarma':
                instance.has_company = True
                instance.save()
            else:
                return {'info': 'method_not_allowed', 'errors': True}
            return {'info': instance, 'errors': False}
        else:
            return {'info': errors, 'errors': True}

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()


class RefreshToken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at + timedelta(days=settings.JWT_CONF['REFRESH_TOKEN_LIFETIME_DAYS']) <= timezone.now()


class State(models.Model):
    city_name = models.CharField(max_length=100)
    homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.city_name
