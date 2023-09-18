from django.contrib import admin
from .models import Job , JobInfo , JobCategory , City , JobSkill , JobFacilitie


admin.site.register([Job , JobCategory , JobInfo , City , JobSkill , JobFacilitie])