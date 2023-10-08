from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.query import QuerySet
import pytz
from custom_users.models import CustomUser
from django.utils import timezone
from django.db.models import Q


class JobQuerySet(models.QuerySet):

    def search(self, query, state, category):
        if state is None:
            state = ''
        lookup_title = Q(title__icontains=query)
        lookup_description = Q(description__icontains=query)
        lookup_state = Q(state__icontains=state)
        qs = Job.objects.filter(lookup_title | lookup_description)
        qs = qs.filter(lookup_state)
        if category:
            lookup_category = Q(category__category__icontains=category)
            qs = qs.filter(lookup_category)
        return qs.order_by('-created')


class JobManager(models.Manager):

    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def search(self, query, state, category):
        return self.get_queryset().search(query, state, category)


class Job(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    work_time = models.CharField(max_length=250)
    work_days = models.CharField(max_length=250)
    income_range = models.CharField(max_length=250)
    image = models.FileField(blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    telecommuting = models.BooleanField(default=False)
    military_order = models.BooleanField(default=False)
    gender = models.CharField(max_length=100)
    min_age = models.CharField(blank=True, null=True, max_length=250)
    max_age = models.CharField(blank=True, null=True, max_length=250)
    hire_intern = models.BooleanField(default=False)
    work_experience = models.CharField(max_length=100)
    hire_military_service = models.BooleanField(default=False)
    hire_disability = models.BooleanField(default=False)
    education_group = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    facilitie = models.ManyToManyField('jobads.JobFacilitie')
    tags = models.CharField(max_length=500)
    business_trip = models.CharField(max_length=100)
    category = models.ManyToManyField('jobads.JobCategory')
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title


class JobCategory(models.Model):
    category = models.CharField(max_length=250)
    homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.category


class JobSkill(models.Model):
    skill = models.CharField(max_length=100)
    level = models.CharField(max_length=100, blank=True)
    job_post = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skill')

    def __str__(self):
        return f'{self.skill} | {self.level} | {self.job_post}'


class JobFacilitie(models.Model):
    facilitie = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.facilitie}'


class CV(models.Model):
    file_name = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_sent_cv')
    status = models.CharField(max_length=250, default='sent')
    jobad = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='cv')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} | {self.jobad} | {self.status}'


class JobCity(models.Model):
    city = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.city}'

class JobState(models.Model):
    state = models.CharField(max_length=250, unique=True)
    related_city = models.ManyToManyField(JobCity)

    def __str__(self):
        return f'{self.state}'