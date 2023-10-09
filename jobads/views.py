from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, JobCategory, JobManager, JobState
from jobads.models import CV
from aloestekhdam.custom_jwt import JWTAuthentication
from rest_framework.permissions import AllowAny
from custom_users.models import CustomUser
from .serializers import JobSerializer, JobStateSerializer


class JobListViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        data = Job.objects.filter().order_by('-created')

        if str(user) != 'AnonymousUser':
            user_data = CustomUser.objects.filter(phone_number=user).first()
            cv_data = CV.objects.filter(jobad__in=data)
            cv_status_dict = {}

            for cv in cv_data:
                if cv.user == user:
                    cv_status_dict[cv.jobad.id] = {
                        'sended': True,
                        'status': cv.status
                    }

        s_data = JobSerializer(data, many=True).data
        for job_data in s_data:
            job_id = job_data['id']
            try:
                if job_id in cv_status_dict:
                    job_data['cv_status'] = cv_status_dict[job_id]
                else:
                    job_data['cv_status'] = {}
            except:
                pass

        return Response(s_data, status=status.HTTP_200_OK)


class JobRetrieveViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = request.user
        data = Job.objects.filter(slug=slug).first()
        if str(user) != 'AnonymousUser':
            user_data = CustomUser.objects.filter(phone_number=user).first()
            cv_data = CV.objects.filter(jobad=data)
            cv_status = {}
            for cv in cv_data:
                if cv.user == user:
                    cv_status['sended'] = True
                    cv_status['status'] = cv.status
        if data != None:
            s_data = JobSerializer(data).data
            try:
                s_data['cv_status'] = cv_status
            except:
                pass
            return Response(s_data, status=status.HTTP_200_OK)
        return Response({'error': 'page_not_found'}, status=status.HTTP_404_NOT_FOUND)


class JobSearchViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        user_query = request.GET.get('q')
        if user_query == None:
            user_query = ''
        user_state = request.GET.get('state')
        user_category = request.GET.get('category')
        data = JobManager().search(query=user_query, state=user_state, category=user_category)
        if str(user) != 'AnonymousUser':
            user_data = CustomUser.objects.filter(phone_number=user).first()
            cv_data = CV.objects.filter(jobad__in=data)
            cv_status_dict = {}

            for cv in cv_data:
                if cv.user == user:
                    cv_status_dict[cv.jobad.id] = {
                        'sended': True,
                        'status': cv.status
                    }
        if data:
            s_data = JobSerializer(data, many=True).data
            for job_data in s_data:
                job_id = job_data['id']
                try:
                    if job_id in cv_status_dict:
                        job_data['cv_status'] = cv_status_dict[job_id]
                    else:
                        job_data['cv_status'] = {}
                except:
                    pass
            return Response(s_data, status=status.HTTP_200_OK)
        return Response({'error': 'nothing_found'}, status=status.HTTP_404_NOT_FOUND)


class GetStateViewSet(APIView):

    def get(self, request):
        try:
            state = request.GET.get('name')
        except:
            return Response({'error': 'name_is_required'}, status=status.HTTP_400_BAD_REQUEST)
        data = JobState.objects.filter(state=state)
        if data:
            s_data = JobStateSerializer(instance=data, many=True).data
            return Response(s_data, status=status.HTTP_200_OK)
        return Response({'error': 'state_name_not_found'}, status=status.HTTP_404_NOT_FOUND)
