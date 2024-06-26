from django.contrib.auth import get_user_model
from django.core.cache import cache

from custom_users.models import CustomUser, State
from custom_users.serializers import UserSerializer, CodeSerializer
from aloestekhdam.tokens import generate_tokens
from django.conf import settings
from rest_framework.views import APIView
from django.db.models.functions import Length

from utils.otp import OTPManager
from utils.regex import user_type_regex
from .createslug import ConvertSlug
from jobads.models import Job, JobCategory, JobFacilitie, JobSkill, CV
from jobads.serializers import JobSerializer, CVSerializer, GetCVUserSerializer, JobLessSerializer, JobDemoSerializer
from rest_framework.response import Response
from aloestekhdam.custom_jwt import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework import status
from json import loads
from rest_framework.permissions import IsAuthenticated
from random import randint
from datetime import datetime
from django.db.models import Q

User = get_user_model()

OTPManager = OTPManager()


class SendOtpCode(APIView):

    def post(self, request):
        user_value = request.POST.get('user_type', 'default')
        method = request.POST.get('method', None)

        status_result, user_type_result = user_type_regex(user=user_value)
        if not status_result:
            return Response({'error': 'Invalid selection'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            user_profile = User.objects.get(Q(phone_number=user_value) | Q(email=user_value))
        except User.DoesNotExist:
            if not method:
                return Response({"You should select method because user dose not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

            elif user_type_result == 'phone':
                User.objects.create(phone_number=user_value, user_type=method)

        user_data = {"value": user_value}
        otp_key = f'otp_type:{user_value}'
        if cache.has_key(otp_key):
            cached_data = cache.get(otp_key)
            cached_otp_token, cached_expiration_time = cached_data
            time_remaining = max((cached_expiration_time - datetime.now()).total_seconds(), 0)
            time_remaining_minutes = int(time_remaining // 60)
            time_remaining_seconds = int(time_remaining % 60)
            return Response(
                {
                    'error': 'OTP already generated. Please wait to resend OTP.',
                    'time_remaining_minutes': time_remaining_minutes,
                    'time_remaining_seconds': time_remaining_seconds
                }, status=status.HTTP_400_BAD_REQUEST
            )

        otp_token, expiration_time = OTPManager.generate_otp(user_data=user_data)
        otp = str(randint(1000, 9000))

        OTPManager.send_sms_to_user(phone_number=user_value, code=otp)
        time_remaining = (expiration_time - datetime.now()).total_seconds()
        time_remaining_minutes = int(time_remaining // 60)
        time_remaining_seconds = int(time_remaining % 60)

        if settings.DEBUG == True:
            return Response({
                'data': "Otp Token was send",
                'expiration_time_minutes': time_remaining_minutes,
                'expiration_time_seconds': time_remaining_seconds,
                'otp_code(it just work on debug mode)': otp_token
            })

        return Response({
            'data': "Otp Token was send",
            'expiration_time_minutes': time_remaining_minutes,
            'expiration_time_seconds': time_remaining_seconds
        })


class VerifyCode(APIView):
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():

            validated_user = serializer.validated_data['user']
            validated_code = serializer.validated_data['code']

            status_result, user_type_result = user_type_regex(user=validated_user)

            user_data = {"value": validated_user}

            if not status_result:
                return Response({'error': 'Invalid selection'}, status=status.HTTP_400_BAD_REQUEST)
            get_user_instance = User.objects.filter(Q(phone_number=validated_user) | Q(email=validated_user)).first()

            if not get_user_instance:
                return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
            validate_otp_result = OTPManager.verify_otp(user_data=user_data, otp_code=validated_code)

            if validate_otp_result[0] == False or None:
                return Response({'error': "Code is wrong"}, status=status.HTTP_400_BAD_REQUEST)

            access_token, refresh_token = JWTAuthentication.create_jwt(get_user_instance)

            return Response({'data': 'Code is correct', 'access_token': access_token, 'refresh_token': refresh_token},
                            status=status.HTTP_200_OK)

        return Response({'error', 'not valid data'}, status=status.HTTP_400_BAD_REQUEST)


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
        if data != None and check_password(password, data.password):
            tokens = JWTAuthentication.create_jwt(data)
            tokens = {
                'refresh': tokens[1],
                'access': tokens[0]
            }
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'phone_number_or_password_is_invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class CheckLoginViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


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

            slug = ConvertSlug(title)
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
        user = CustomUser.objects.filter(phone_number=request.user).first()
        user_data = request.data
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

        try:
            title = user_data['title']
            work_time = user_data['work_time']
            state = user_data['state']
            city = user_data['city']
            income_range = user_data['income_range']
            work_experience = user_data['work_experience']
            work_days = user_data['work_days']
            description = user_data['description']
            slug = user_data['slug']
        except KeyError as e:
            return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)

        if slug:
            if user.has_company:
                category = request.data.get('category')
                category_obj = JobCategory.objects.filter(category=category).first()
                if category_obj is None:
                    return Response({'error': 'category_not_found'}, status=status.HTTP_404_NOT_FOUND)

                if user_data.get('facilitie'):
                    facilities = user_data.get('facilitie').split(',')
                    facilitie = []
                    status_facilitie = True
                    if facilities:
                        for facilitie_name in facilities:
                            facilitie_obj = JobFacilitie.objects.filter(facilitie=facilitie_name).first()
                            if facilitie_obj is None:
                                return Response({'error': 'facilitie_not_found'}, status=status.HTTP_404_NOT_FOUND)
                            facilitie.append(facilitie_obj)

                job_data = Job.objects.filter(owner=user, slug=slug).first()

                slug = ConvertSlug(title)

                if job_data:
                    if request.data.get('job_skills'):
                        job_skills = loads(request.data['job_skills'])
                        for json_skills in job_skills:
                            skill = json_skills['skill']
                            level = json_skills['level']
                            skill_obj = JobSkill.objects.update_or_create(
                                skill=skill,
                                level=level,
                                job_post=job_data
                            )
                    else:
                        skill_obj = JobSkill.objects.filter(job_post=job_data)
                        for skill in skill_obj:
                            skill.delete()

                    job_data.title = title
                    job_data.work_time = work_time
                    job_data.state = state
                    job_data.city = city
                    job_data.income_range = income_range
                    job_data.work_experience = work_experience
                    job_data.work_days = work_days
                    job_data.description = description
                    job_data.slug = slug
                    job_data.status = False
                    for o_field in optional_fields:
                        for u_field in user_data:
                            if u_field == o_field:
                                setattr(job_data, u_field, request.data[u_field])

                    job_data.category.set([category_obj])
                    if status_facilitie:
                        job_data.facilitie.set(facilitie)
                    job_data.save()

                    return Response({'success': f'{title}_has_been_updated'}, status=status.HTTP_200_OK)
                return Response({'error': 'job_not_found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'job_slug_is_empty'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user_data = request.data
        user_job_slug = request.data.get('slug')
        if user_job_slug:
            data = Job.objects.filter(owner=user, slug=user_job_slug)
            if data:
                data.delete()
                return Response({'success': f'{user_job_slug}_is_deleted'}, status=status.HTTP_200_OK)
            return Response({'error': 'job_not_found'}, status=status.HTTP_404_NOT_FOUND)
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
        cv_file = f"{settings.DEFAULT_IMAGE_URL}{user_data.user_cv}"
        job_data = Job.objects.filter(slug=request.data['slug'], status=True).first()
        if user_data and job_data and cv_file:
            if not user_data.has_company:
                data = CV.objects.create(
                    file_name=cv_file,
                    jobad=job_data,
                    first_name=user_data.username,
                    job_slug=job_data.slug,
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
        if not user.has_company:
            cvs = CV.objects.filter(user=user).order_by('-id')
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
        user_data = request.user
        if user_data.has_company:
            method = request.GET.get('method')
            if not method:
                method = 'sent'
            if method == 'sent':
                user_cv = CV.objects.filter(owner=user_data, status='sent').order_by('-id')
            elif method == 'confirmed':
                user_cv = CV.objects.filter(owner=user_data, status='confirmed').order_by('-id')
            elif method == 'failed':
                user_cv = CV.objects.filter(owner=user_data, status='failed').order_by('-id')
            else:
                return Response({'error': {'accepted_methods': ['sent', 'confirmed', 'failed']}},
                                status=status.HTTP_400_BAD_REQUEST)

            s_user_cv = CVSerializer(user_cv, many=True).data
            return Response(s_user_cv, status=status.HTTP_200_OK)
        return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)


class EditCompanyCVViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_data = CustomUser.objects.filter(phone_number=request.user).first()
        editable_status = [
            'confirmed',
            'failed'
        ]

        if user_data.has_company:
            try:
                id = request.data['id']
                cv_status = request.data['cv_status']
            except Exception as e:
                e = str(e).replace("'", '', -1)
                return Response({'error': f'{e}_is_required'}, status=status.HTTP_400_BAD_REQUEST)
            if cv_status in editable_status:
                user_cv = CV.objects.filter(owner=user_data, id=id).first()
                if user_cv:
                    user_cv.status = cv_status
                    user_cv.save()
                    return Response({'success': 'cv_edited'}, status=status.HTTP_200_OK)
        return Response({'error': 'access_denied'}, status=status.HTTP_401_UNAUTHORIZED)


class GetCompanyAdsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        job_data = Job.objects.filter(owner=user).order_by('-created')
        s_job_data = JobLessSerializer(job_data, many=True).data
        return Response(s_job_data, status=status.HTTP_200_OK)


class CompanyAdDemoViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        user = request.user
        if slug == '':
            return Response({'error': 'slug_is_empty'}, status=status.HTTP_400_BAD_REQUEST)

        data = Job.objects.filter(owner=user, slug=slug).order_by('-created').first()
        s_data = JobDemoSerializer(data).data
        return Response(s_data, status=status.HTTP_200_OK)
