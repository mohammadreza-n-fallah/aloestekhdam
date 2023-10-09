from custom_users.models import CustomUser, State
from custom_users.serializers import UserSerializer
from aloestekhdam.tokens import generate_tokens
from rest_framework.views import APIView
from .verify import send_verify_code
from jobads.models import Job, JobCategory, JobFacilitie, JobSkill, CV
from jobads.serializers import JobSerializer, CVSerializer, GetCVUserSerializer
from rest_framework.response import Response
from aloestekhdam.custom_jwt import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework import status
from json import loads
from rest_framework.permissions import IsAuthenticated
from random import randint
from datetime import datetime


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
            return Response({'error': f'{e} field is required'}, status=status.HTTP_400_BAD_REQUEST)
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
            verify_code = request.data['password']
        except:
            return Response({'error': 'phone_number_or_verify_code_is_empty'}, status=status.HTTP_400_BAD_REQUEST)
        data = CustomUser.objects.filter(phone_number=phone_number).first()
        code = send_verify_code()
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
        if data:
            return Response({'success': 'phone_number_ok'}, status=status.HTTP_200_OK)
        return Response({'error': 'phone_number_not_found'}, status=status.HTTP_404_NOT_FOUND)


class GetUserDataViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = CustomUser.objects.filter(phone_number=user).first()
        s_data = UserSerializer(data).data
        return Response(s_data)


class JobCreateViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.user
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        optional_fields = [
            'telecommuting',
            'education_group',
            'education_level',
            'military_order',
            'min_age',
            'max_age',
            'gender',
            'hire_intern',
            'hire_military_service',
            'hire_disability',
            'business_trip',
        ]
        status_facilitie = False
        if user.has_company == True:
            user_data = request.data
            try:
                title = user_data['title']
                work_time = user_data['work_time']
                state = user_data['state']
                city = user_data['city']
                income_range = user_data['income_range']
                work_experience = user_data['work_experience']
                work_days = user_data['work_days']
                description = user_data['description']

            except KeyError as e:
                e = str(e).replace("'", "", -1)
                return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)

            category = request.data.get('category')
            category_obj = JobCategory.objects.filter(category=category).first()
            if category_obj is None:
                return Response({'error': 'category_not_found'}, status=status.HTTP_404_NOT_FOUND)

            if request.data.get('facilitie'):
                facilities = request.data.get('facilitie').split(',')
                facilitie = []
                status_facilitie = True
                if facilities:
                    for facilitie_name in facilities:
                        facilitie_obj = JobFacilitie.objects.filter(facilitie=facilitie_name).first()
                        if facilitie_obj is None:
                            return Response({'error': 'facilitie_not_found'}, status=status.HTTP_404_NOT_FOUND)
                        facilitie.append(facilitie_obj)

            slug = f"{title.replace(' ', '-', -1)}-{datetime.now().year}-{datetime.now().month}-{datetime.now().day}-{datetime.now().microsecond}"
            print (user.image)
            data = Job.objects.create(
                title=title,
                work_time=work_time,
                state=state,
                city=city,
                owner=user,
                image=user.image,
                income_range=income_range,
                work_experience=work_experience,
                work_days=work_days,
                description=description,
                status=False,
                slug=slug,
            )

            if request.data.get('job_skills'):
                job_skills = loads(request.data['job_skills'])
                for json_skills in job_skills:
                    skill = json_skills['skill']
                    level = json_skills['level']
                    skill_obj = JobSkill.objects.create(
                        skill=skill,
                        level=level,
                        job_post=data
                    )

            data.category.set([category_obj])
            if status_facilitie:
                data.facilitie.set(facilitie)

            for o_field in optional_fields:
                for u_field in request.data:
                    if u_field == o_field:
                        setattr(data, u_field, request.data[u_field])
            data.save()
            return Response({'success': f'{title}_is_created'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'user_has_no_company'}, status=status.HTTP_406_NOT_ACCEPTABLE)


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
        user = request.user
        user = CustomUser.objects.filter(phone_number=user).first()
        if user.has_company:
            try:
                full_name = request.data['full_name']
                company_name = request.data['company_name']
                organization_side = request.data['organization_side']
                organization_size = request.data['organization_size']
                phone_number_2 = request.data['phone_number_2']
                company_telephone = request.data['company_telephone']
                type_of_activity = request.data['type_of_activity']
                established_year = request.data['established_year']
                brand = request.data['brand']
                ownership = request.data['ownership']
                state = request.data['state']
                industry = request.data['industry']
                service_and_products = request.data['service_and_products']
                description_of_company = request.data['description_of_company']
            except KeyError as e:
                return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)
            user.company_name = company_name
            user.full_name = full_name
            user.organization_size = organization_size
            user.type_of_activity = type_of_activity
            user.established_year = established_year
            user.organization_side = organization_side
            user.phone_number_2 = phone_number_2
            user.company_telephone = company_telephone
            user.brand = brand
            user.industry = industry
            user.service_and_products = service_and_products
            user.description_of_company = description_of_company
            user.ownership = ownership

            state_model = State.objects.filter(city_name=state).first()
            if state_model != None:
                user.state = state_model
            try:
                user.website = request.data['website']
            except:
                pass
            try:
                user.company_telephone_2 = request.data['company_telephone_2']
            except:
                pass
            if request.data.get('image'):
                if len(request.data.get('image')) != 0:
                    user.image = request.data['image']
                if request.data['image'] == 'remove':
                    user.image = None
            user.save()

            return Response({'success': f'user_company_updated'}, status=status.HTTP_200_OK)

        return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)


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


class AddCVToUserViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            cv_file = request.data['cv_file']
        except:
            return Response({'error': 'cv_file_is_required'}, status=status.HTTP_400_BAD_REQUEST)

        if cv_file.name.split('.')[-1].lower() == 'pdf':
            user = CustomUser.objects.filter(phone_number=request.user).first()
            user.user_cv = cv_file
            user.save()
            return Response({'success': 'cv_file_uploaded'}, status=status.HTTP_200_OK)
        return Response({'error': 'somthing_went_wrong'}, status=status.HTTP_400_BAD_REQUEST)


class SendCVJobViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            slug = request.data['slug']
        except Exception as e:
            e = str(e).replace("'", '', -1)
            return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_data = CustomUser.objects.filter(phone_number=user).first()
        cv_file = f"https://storage.avalamozesh.com/aloestekhdam/{user_data.user_cv}"
        job_data = Job.objects.filter(slug=request.data['slug']).first()
        if user_data and job_data and cv_file:
            if not user_data.has_company:
                data = CV.objects.create(
                    file_name=cv_file,
                    jobad=job_data,
                    user=user_data,
                    owner=job_data.owner
                )
                return Response({'success': 'cv_sent'}, status=status.HTTP_200_OK)
            return Response({'error': 'not_allowed'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'user_or_job_not_found'}, status=status.HTTP_404_NOT_FOUND)


class GetUserCVsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_query = CustomUser.objects.filter(phone_number=user).first()
        if not user_query.has_company:
            cvs = CV.objects.filter(user=user_query)
            if cvs:
                s_data = GetCVUserSerializer(cvs, many=True).data
                return Response(s_data, status=status.HTTP_200_OK)
            return Response({'error': 'there_is_no_cv_for_this_user'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'access_denied'}, status=status.HTTP_400_BAD_REQUEST)


class IsCompanyInfoCompleteViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = CustomUser.objects.filter(phone_number=user).first()

        if user_data.has_company:
            requirement_list = [
                'company_name',
                'full_name',
                'organization_size',
                'type_of_activity',
                'established_year',
                'organization_side',
                'phone_number_2',
                'company_telephone',
                'brand',
                'industry',
                'service_and_products',
                'description_of_company',
                'ownership'
            ]

            missing_fields = [field for field in requirement_list if not getattr(user_data, field)]

            if not missing_fields:
                return Response({True}, status=status.HTTP_200_OK)
            else:
                return Response({False}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({False}, status=status.HTTP_401_UNAUTHORIZED)


class GetCompanyCVViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = CustomUser.objects.filter(phone_number=request.user).first()
        print (user_data)
        if user_data.has_company:
            user_cv = CV.objects.filter(owner=user_data)
            s_user_cv = CVSerializer(user_cv, many=True).data
            return Response(s_user_cv, status=status.HTTP_200_OK)
        return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)
    

class EditCompanyCVViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_data = CustomUser.objects.filter(phone_number=request.user).first()
        editable_status = [
            'reviewed',
            'failed'
        ]

        if user_data.has_company:
            try:
                id = request.data['id']
                cv_status = request.data['cv_status']
            except Exception as e:
                e = str(e).replace("'" , '' , -1)
                return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)
            if cv_status in editable_status:
                user_cv = CV.objects.filter(owner=user_data,id=id).first()
                if user_cv:
                    user_cv.status = cv_status
                    user_cv.save()
                    return Response({'success': 'cv_edited'}, status=status.HTTP_200_OK)
        return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)