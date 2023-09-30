from custom_users.models import CustomUser
from custom_users.serializers import UserSerializer
from aloestekhdam.tokens import generate_tokens
from rest_framework.views import APIView
from jobads.models import Job, JobCategory, JobFacilitie, JobSkill
from jobads.serializers import JobSerializer
from rest_framework.response import Response
from aloestekhdam.custom_jwt import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from random import randint


class SignUpViewSet(APIView):

    def post(self, request):
        try:
            username = f'user_{randint(1, 1000)}'
            password = request.data['password']
            method = request.data['method']
            phone_number = request.data['phone_number']
            user_type = 'causal'
        except KeyError as e:
            e = str(e).replace("'", '', -1)
            return Response({'error': f'{e} field is require'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = CustomUser.save_user(username, password, phone_number, user_type, method)
            token = JWTAuthentication.create_jwt(data['info'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if data['errors'] != True:
            s_data = UserSerializer(data['info']).data
            return Response({'refresh': token[0], 'access': token[1]}, status=status.HTTP_201_CREATED)
        return Response({'info': data['info']}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):

    def post(self, request):
        try:
            phone_number = request.data['phone_number']
            password = request.data['password']
        except:
            return Response({'error': 'phone_number_or_password_is_empty'}, status=status.HTTP_400_BAD_REQUEST)
        data = CustomUser.objects.filter(phone_number=phone_number).first()
        if data != None and check_password(password, data.password):
            tokens = JWTAuthentication.create_jwt(data)
            tokens = {
                'refresh': tokens[1],
                'access': tokens[0]
            }
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'phone_number_or_password_is_invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class CheckNumberLoginViewSet(APIView):

    def get(self, request):
        phone_number = str()
        try:
            phone_number = request.GET.get('phone_number')
        except:
            return Response({'error': 'phone_number_is_empty'}, status=status.HTTP_400_BAD_REQUEST)

        data = CustomUser.objects.filter(phone_number=phone_number).first()
        print(data)
        if data:
            return Response({'success': 'phone_number_ok'}, status=status.HTTP_200_OK)
        return Response({'error': 'phone_number_not_found'}, status=status.HTTP_404_NOT_FOUND)


class GetUserDataViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = CustomUser.objects.filter(username=user.username).first()
        s_data = UserSerializer(data).data
        return Response(s_data)


class JobCreateViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.user
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user != None:
            if user.has_company == True:
                user_data = request.data
                try:
                    title = user_data['title']
                    description = user_data['description']
                    work_time = user_data['work_time']
                    work_days = user_data['work_days']
                    city = user_data['city']
                    gender = user_data['gender']
                    work_experience = user_data['work_experience']
                    education_group = user_data['education_group']
                    education_level = user_data['education_level']
                    business_trip = user_data['business_trip']
                    max_age = user_data['max_age']
                    min_age = user_data['min_age']
                    cooperation = user_data['cooperation']
                    income_range = user_data['income_range']
                    location = user_data['location']
                    owner = user
                    tags = user_data['tags']
                    category = JobCategory.objects.filter(category=user_data['category']).first()
                    state = user.state.all().first()
                    jobfacilitie = JobFacilitie.objects.filter(facilitie=user_data['jobfacilitie']).first()
                    job_skill = user_data['job_skill']
                    job_level = user_data['job_level']
                    slug = title
                except Exception as e:
                    e = str(e).replace("'", "", -1)
                    return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)
                if category != None and jobfacilitie != None:
                    data = Job.objects.create(
                        title=title,
                        description=description,
                        work_time=work_time,
                        max_age=max_age,
                        cooperation=cooperation,
                        min_age=min_age,
                        work_days=work_days,
                        state=state,
                        gender=gender,
                        work_experience=work_experience,
                        education_group=education_group,
                        education_level=education_level,
                        business_trip=business_trip,
                        income_range=income_range,
                        location=location,
                        city=city,
                        owner=owner,
                        tags=tags,
                        slug=slug,
                        status='waiting-confirm',
                    )
                    data.category.set([category])
                    data.facilitie.set([jobfacilitie])
                    JobSkill.objects.create(
                        skill=job_skill,
                        level=job_level,
                        job_post=data
                    )
                    return Response({'sucess': f'{title}_is_created'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response({'error': 'category_not_found'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'error': 'user_has_no_company'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'error': 'user_not_found'}, status=status.HTTP_401_UNAUTHORIZED)


class JobModifyViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        username = request.user
        user_data = request.data
        user_job_slug = user_data['job_slug']
        try:
            title = user_data['title']
            description = user_data['description']
            work_time = user_data['work_time']
            income_range = user_data['income_range']
            location = user_data['location']
            tags = user_data['tags']
            category = JobCategory.objects.filter(category=user_data['category']).first()
            slug = user_data['slug']
        except KeyError as e:
            return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)

        if user_job_slug:
            owner = CustomUser.objects.filter(username=username).first()
            user_job = Job.objects.filter(owner=owner, slug=user_job_slug)
            user_job.update(
                title=title,
                description=description,
                work_time=work_time,
                income_range=income_range,
                location=location,
                owner=owner,
                tags=tags,
                slug=slug,
            )
            if category:
                user_job.first().category.set([category])
            return Response({'success': f'{title}_has_been_updated'}, status=status.HTTP_200_OK)

        return Response({'error': 'job_slug_is_empty'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        username = request.user
        user_data = request.data
        user_job_slug = user_data['job_slug']
        if user_job_slug:
            data = Job.objects.filter(owner__username=username, slug=user_job_slug).delete()
            return Response({'success': f'{user_job_slug}_is_deleted'}, status=status.HTTP_200_OK)

        return Response({'error': 'job_slug_is_empty'}, status=status.HTTP_400_BAD_REQUEST)


class AddAndEditUserCompamyViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        username = request.user
        user = CustomUser.objects.filter(username=username).first()
        if user:
            user_data = request.data
            try:
                company_name = user_data['company_name']
                organization_size = user_data['organization_size']
                type_of_activity = user_data['type_of_activity']
                established_year = user_data['established_year']
                ownership = user_data['ownership']
            except KeyError as e:
                return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)

            user.has_company = True
            user.company_name = company_name
            user.organization_size = organization_size
            user.type_of_activity = type_of_activity
            user.established_year = established_year
            user.ownership = ownership
            user.save()

            return Response({'success': f'{company_name}_is_created'}, status=status.HTTP_200_OK)

        return Response({'error': 'user_not_found'}, status=status.HTTP_401_UNAUTHORIZED)


class EditUserProfileViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = CustomUser.objects.filter(phone_number=request.user)
        if user.first():
            editable_fields = [
                'username',
                'email',
                'image',
            ]
            image_formats = [
                'png',
                'webp',
                'jpg',
                'jpeg',
            ]
            user_data = list(request.data)
            for udata in user_data:
                for edata in editable_fields:
                    if udata == edata:
                        if udata == 'image':
                            user_image = request.data['image']
                            image_extension = user_image.name.split('.')[-1].lower()
                            if image_extension not in image_formats:
                                return Response({'error': 'file_input_is_invalid'}, status=status.HTTP_403_FORBIDDEN)
                        s_data = UserSerializer(instance=user.first(), data=request.data, partial=True)
                        if s_data.is_valid():
                            s_data.save()
                        else:
                            return Response({'error': 'input_is_not_valid'}, status=status.HTTP_403_FORBIDDEN)
                        return Response({'success': 'user_updated'}, status=status.HTTP_200_OK)
            return Response({'error': 'access_denied'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)


class GetUserAdsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user
        query = request.GET.get('status')
        user = CustomUser.objects.filter(username=username).first()
        if query == 'all':
            data = Job.objects.filter(owner=user)
        else:
            data = Job.objects.filter(owner=user, status=query)
        if data != None:
            s_data = JobSerializer(data, many=True).data
            return Response(s_data, status=status.HTTP_200_OK)
        return Response({'error': 'data_not_found'}, status=status.HTTP_404_NOT_FOUND)
