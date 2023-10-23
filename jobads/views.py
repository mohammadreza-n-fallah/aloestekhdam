from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, JobCategory, JobManager, JobState, JobIncome, JobTime
from aloestekhdam.custom_jwt import JWTAuthentication
from rest_framework.permissions import AllowAny
from .serializers import JobSerializer, JobStateSerializer, JobIncomeSerializer, JobTimeSerializer
from .usercv import CheckCv


class JobListViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        data = Job.objects.filter(status=True).order_by('-created')

        if str(user) != 'AnonymousUser':
            result = CheckCv(user, data)
        else:
            result = JobSerializer(data, many=True).data
        
        result = [
        {
            'id': item['id'],
            'title': item['title'],
            'income_range': item['income_range'],
            'company_name': item['company_info']['company_name'],
            'work_time': item['work_time'],
            'state': item['state'],
            'city': item['city'],
            'slug': item['slug'],
            'image': item['image'],
            'cv_status': item.get('cv_status', None)
        }
        for item in result
        ]

        return Response(result, status=status.HTTP_200_OK)


class JobRetrieveViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = request.user
        data = Job.objects.filter(status=True, slug=slug)
        if data:
            if str(user) != 'AnonymousUser':
                result = CheckCv(user, data)[0]
            else:
                data = data.first()
                result = JobSerializer(data).data
            return Response(result, status=status.HTTP_200_OK)
        return Response({'error': 'job_not_found'}, status=status.HTTP_404_NOT_FOUND)



class JobSearchViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        user_query = request.GET.get('q')
        if user_query == None:
            user_query = ''
        user_state = request.GET.get('state', '')
        user_category = request.GET.get('category', '')
        user_income_range = request.GET.get('income_range', '')
        user_work_time = request.GET.get('work_time', '')
        data = JobManager().search(
            query=user_query, 
            state=user_state, 
            category=user_category, 
            income_range=user_income_range, 
            work_time=user_work_time
            )

        if data:
            if str(user) != 'AnonymousUser':
                result = CheckCv(user, data)
            else:
                result = JobSerializer(data, many=True).data
            result = [
                    {
                        'id': item['id'],
                        'title': item['title'],
                        'income_range': item['income_range'],
                        'company_name': item['company_info']['company_name'],
                        'work_time': item['work_time'],
                        'state': item['state'],
                        'city': item['city'],
                        'slug': item['slug'],
                        'image': item['image'],
                        'cv_status': item.get('cv_status', None)
                    }
                    for item in result
                ]
            return Response(result, status=status.HTTP_200_OK)
        return Response({'error': 'nothing_found'}, status=status.HTTP_404_NOT_FOUND)


class GetStateViewSet(APIView):
    

    def get(self, request):
        state = request.GET.get('name')
        
        if not state:
            data = JobState.objects.filter().values_list('state', flat=True)
            return Response(data, status=status.HTTP_200_OK)
        
        data = JobState.objects.filter(state=state)

        if data:
            s_data = JobStateSerializer(instance=data, many=True).data[0]['related_city']
            return Response(s_data, status=status.HTTP_200_OK)

        return Response({'error': 'state_name_not_found'}, status=status.HTTP_404_NOT_FOUND)
    


class GetRelatedJobsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        category = JobCategory.objects.filter(category=request.GET.get('category')).first()
        slug = request.GET.get('slug')
        if category is None and not slug:
            return Response({'error': {'required_params': ['category', 'slug']}})
        
        data = Job.objects.filter(status=True, category=category).exclude(slug=slug)

        if data:
            if len(data) < 5:
                pass
            else:
                data = data[:5:]
                
            if str(user) != 'AnonymousUser':
                result = CheckCv(user, data)
            else:
                result = JobSerializer(data, many=True).data

            result = [
                    {
                        'id': item['id'],
                        'title': item['title'],
                        'income_range': item['income_range'],
                        'company_name': item['company_info']['company_name'],
                        'work_time': item['work_time'],
                        'state': item['state'],
                        'city': item['city'],
                        'slug': item['slug'],
                        'image': item['image'],
                        'cv_status': item.get('cv_status', None)
                    }
                    for item in result
                ]
            return Response(result, status=status.HTTP_200_OK)
        return Response({'error': 'related_job_not_found'}, status=status.HTTP_404_NOT_FOUND)



class GetJobIncomeViewSet(APIView):

    def get(self, request):
        data = JobIncome.objects.filter()
        s_data = JobIncomeSerializer(data, many=True).data
        return Response(s_data, status=status.HTTP_200_OK)
    


class GetJobTimeViewSet(APIView):

    def get(self, request):
        data = JobTime.objects.filter()
        s_data = JobTimeSerializer(data, many=True).data
        return Response(s_data, status=status.HTTP_200_OK)
    


class GetLatestJobsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        data = Job.objects.filter(status=True).order_by('-created')
        if str(user) != 'AnonymousUser':
            result = CheckCv(user, data)[:5:]
        else:
            result = JobSerializer(data, many=True).data[:5:]
        
        result = [
                    {
                        'id': item['id'],
                        'title': item['title'],
                        'income_range': item['income_range'],
                        'company_name': item['company_info']['company_name'],
                        'work_time': item['work_time'],
                        'state': item['state'],
                        'city': item['city'],
                        'slug': item['slug'],
                        'image': item['image'],
                        'cv_status': item.get('cv_status', None)
                    }
                    for item in result
                ]
        return Response(result, status=status.HTTP_200_OK)