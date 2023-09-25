from rest_framework import serializers
from .models import Job , JobInfo , JobCategory , JobSkill




class JobSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField('username' , read_only=True)
    job_info = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)
    city = serializers.StringRelatedField(many=True)
    facilitie = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = '__all__'
    
    def get_job_info(self , obj):
        data = obj.jobinfo.filter()
        return JobInfoSerializer(data , many=True).data

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