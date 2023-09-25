from django.contrib import admin
from .models import Job , JobInfo , JobCategory , JobSkill , JobFacilitie


admin.site.register([Job , JobCategory , JobInfo , JobSkill , JobFacilitie])