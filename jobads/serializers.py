from rest_framework import serializers
from .models import Job , JobInfo , JobCategory , JobSkill
from custom_users.serializers import CompanySerializer
from custom_users.models import CustomUser



class JobSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField('username' , read_only=True)
    job_info = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)
    # city = serializers.StringRelatedField(many=True)
    facilitie = serializers.StringRelatedField(many=True)
    company_info = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
    
    def get_job_info(self , obj):
        data = obj.jobinfo.filter()
        return JobInfoSerializer(data , many=True).data
    def get_company_info(self, obj):
        owner = obj.owner
        custom_user = CustomUser.objects.filter(phone_number=owner).first()
        print (owner)
        if custom_user:
            return CompanySerializer(custom_user).data
        return {}

class JobInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobInfo
        fields = ['id' , 'requirement_text']

class JobCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobCategory
        fields = '__all__'

class JobSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSkill
        fields = []