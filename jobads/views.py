from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job , JobCategory , JobInfo , JobManager
from .serializers import JobSerializer





class JobListViewSet(APIView):

    def get(self , request):
        data = Job.objects.filter().order_by('-created')
        s_data = JobSerializer(data , many = True).data
        return Response(s_data , status=status.HTTP_200_OK)
    



class JobRetrieveViewSet(APIView):

    def get(self , request , slug):
        data = Job.objects.filter(slug=slug).first()
        if data != None:
            s_data = JobSerializer(data).data
            return Response(s_data , status=status.HTTP_200_OK)
        return Response({'error' : 'page_not_found'} , status=status.HTTP_404_NOT_FOUND)
    


class JobSearchViewSet(APIView):
    def get(self, request):
        user_query = request.GET.get('q')
        if user_query:
            data = JobManager().search(query=user_query)
            if data:
                s_data = JobSerializer(data , many = True).data
                return Response(s_data , status=status.HTTP_200_OK)
            return Response({'error' : 'nothing_found'} , status=status.HTTP_404_NOT_FOUND)
        return Response({'error' : 'query_is_empty'} , status=status.HTTP_400_BAD_REQUEST)