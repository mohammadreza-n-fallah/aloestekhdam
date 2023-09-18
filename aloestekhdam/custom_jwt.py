from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework import authentication
from django.conf import settings
import jwt
from custom_users.models import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    @classmethod
    def authenticate(cls, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        username_or_phone_number = payload.get('user_identifier')
        if username_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(phone_number=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        access_token_payload = {
            'user_identifier': user.phone_number,
            'exp': int(
                (datetime.now() + timedelta(hours=settings.JWT_CONF['ACCESS_TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'phone_number': user.phone_number
        }
        refresh_token_payload = {
            'user_identifier': user.phone_number,
            'exp': int((datetime.now() + timedelta(days=settings.JWT_CONF['REFRESH_TOKEN_LIFETIME_DAYS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'phone_number': user.phone_number
        }

        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

        try:
            refresh_token_obj = RefreshToken.objects.get(user=user)
            return access_token, refresh_token

        except RefreshToken.DoesNotExist:
            create_new_isnstance = RefreshToken.objects.create(user=user, token=refresh_token)

            return access_token, refresh_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token