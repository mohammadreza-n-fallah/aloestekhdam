from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.query import QuerySet
from custom_users.models import CustomUser
from django.db.models import Q



class JobQuerySet(models.QuerySet):


    def search(self , query):
        lookup_title = Q(title__icontains=query)
        lookup_description = Q(description__icontains=query)
        qs = Job.objects.filter(lookup_title | lookup_description)
        return qs



class JobManager(models.Manager):

    def get_queryset(self):
        return JobQuerySet(self.model , using=self._db)
    
    def search(self , query):
        return self.get_queryset().search(query)




class Job (models.Model):
    title = models.CharField(max_length=500 , unique=True)
    description = models.TextField()
    work_time = models.CharField(max_length=250)
    work_days = models.CharField(max_length=250)
    cooperation = models.CharField(max_length=100)
    income_range = models.CharField(max_length=250)
    image = models.FileField(blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    owner = models.ForeignKey(CustomUser , on_delete=models.CASCADE , blank=True)
    telecommuting = models.BooleanField(default=False)
    gender = models.CharField(max_length=100)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
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
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=500 , unique=True)

    def __str__(self):
        return self.title



class JobCategory(models.Model):
    category = models.CharField(max_length=250)
    homepage = models.BooleanField(default=False)


    def __str__ (self):
        return self.category


class JobInfo(models.Model):
    job_post = models.ForeignKey(Job , on_delete=models.CASCADE , related_name='jobinfo')
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , blank=True)
    requirement_text = models.CharField(max_length=500)

    def __str__(self):
        return self.requirement_text + '|' + str(self.id)
    





    

class JobSkill(models.Model):
    skill = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    job_post = models.ForeignKey(Job , on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.skill} | {self.level} | {self.job_post}'
    

class JobFacilitie(models.Model):
    facilitie = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.facilitie}'
    

