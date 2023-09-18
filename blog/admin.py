from django.contrib import admin
from .models import Blog , BlogCategory , BlogComment


admin.site.register([Blog , BlogCategory , BlogComment])