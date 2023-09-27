from django.contrib import admin
from .models import CustomUser, RefreshToken, State

admin.site.register([CustomUser, State, RefreshToken])
