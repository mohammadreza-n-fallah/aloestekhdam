from django.contrib import admin
from .models import Job, JobCategory, JobSkill, JobFacilitie, CV, JobState, JobCity

admin.site.register([Job, JobCategory, JobSkill, JobFacilitie, CV, JobState, JobCity])
