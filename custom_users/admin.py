from django.contrib import admin
from .models import CustomUser , RefreshToken


admin.site.register([CustomUser , RefreshToken])