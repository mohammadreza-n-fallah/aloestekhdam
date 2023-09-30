from django.contrib import admin
from .models import Job, JobCategory, JobSkill, JobFacilitie, CV

admin.site.register([Job, JobCategory, JobSkill, JobFacilitie, CV])
