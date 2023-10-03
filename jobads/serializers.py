from rest_framework import serializers
from .models import Job, JobCategory, JobSkill, CV
from django.conf import settings
from custom_users.serializers import CompanySerializer
from custom_users.models import CustomUser


class JobSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField('username', read_only=True)
    category = serializers.StringRelatedField(many=True)
    job_skills = serializers.SerializerMethodField()
    facilitie = serializers.StringRelatedField(many=True)
    company_info = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_cv(self, obj):
        data = obj.cv.filter()
        return CVSerializer(data, many=True).data

    def get_company_info(self, obj):
        owner = obj.owner
        custom_user = CustomUser.objects.filter(phone_number=owner).first()
        if custom_user:
            return CompanySerializer(custom_user).data
        return {}

    def get_job_skills(self, obj):
        data = obj.skill.filter()
        return JobSkillSerializer(data, many=True).data


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'


class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ['skill', 'level']


class CVSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    jobad = serializers.StringRelatedField()

    class Meta:
        model = CV
        fields = '__all__'


class GetCVUserSerializer(serializers.ModelSerializer):
    jobad = serializers.StringRelatedField()
    company_name = serializers.SerializerMethodField()
    company_slug = serializers.SerializerMethodField()
    company_image = serializers.SerializerMethodField()

    class Meta:
        model = CV
        fields = ['jobad', 'status', 'company_name', 'company_slug' ,'company_image', 'created']

    def get_company_image(self, obj):
        data = str(Job.objects.filter(title=obj.jobad).first().image)
        return f'{settings.DEFAULT_IMAGE_URL}{data}'

    def get_company_name(self, obj):
        data = Job.objects.filter(title=obj.jobad).first().owner
        return CustomUser.objects.filter(phone_number=data).first().company_name

    def get_company_slug(self, obj):
        data = str(Job.objects.filter(title=obj.jobad).first().slug)
        return data
