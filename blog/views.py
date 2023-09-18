from django.shortcuts import render
from .models import Blog , BlogComment
from custom_users.models import CustomUser
from .serializers import BlogSerializer , BlogListSerializer , BlogCommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



class BlogListViewSet(APIView):

    def get(self , request):
        data = Blog.objects.filter().order_by('-created')
        s_data = BlogListSerializer(data , many = True).data
        return Response(s_data , status=status.HTTP_200_OK)
    
class BlogRetrieveViewSet(APIView):

    def get(self, request, slug):
        data = Blog.objects.filter(slug=slug).first()
        if data:
            s_data = BlogSerializer(data).data
            return Response(s_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    



    
