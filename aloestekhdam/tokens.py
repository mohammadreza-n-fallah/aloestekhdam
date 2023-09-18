from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    user.token = str(access_token)
    user.save()
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }