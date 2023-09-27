from django.contrib import admin
from .models import Job, JobCategory, JobSkill, JobFacilitie

admin.site.register([Job, JobCategory, JobSkill, JobFacilitie])
