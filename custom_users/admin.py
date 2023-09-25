from django.contrib import admin
from .models import CustomUser , RefreshToken , City


admin.site.register([CustomUser , City , RefreshToken])