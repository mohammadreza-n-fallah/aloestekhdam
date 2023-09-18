from django.urls import path
from . import views

urlpatterns = [
    path ('signup/' , views.SignUpViewSet.as_view()),
    path ('login/' , views.LoginViewSet.as_view()),
    path ('check_phone_number' , views.CheckNumberLoginViewSet.as_view()),
    path ('user_data' , views.GetUserDataViewSet.as_view()),
    path ('create_job/' , views.JobCreateViewSet.as_view()),
    path ('modify_company/' , views.AddAndEditUserCompamyViewSet.as_view()),
    path ('modify_job/' , views.JobModifyViewSet.as_view()),
    path ('create_job_info/' , views.JobInfoCreate.as_view()),
    path ('modify_job_info/' , views.JobInfoModify.as_view()),
    path ('get_user_ads' , views.GetUserAdsViewSet.as_view()),
]