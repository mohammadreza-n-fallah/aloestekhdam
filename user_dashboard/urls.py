from django.urls import path
from . import views

urlpatterns = [
    path('send-code/', views.SendOtpCode.as_view()),
    path('verify-code/', views.VerifyCode.as_view()),
    path('signup/', views.SignUpViewSet.as_view()),
    path('login/', views.LoginViewSet.as_view()),
    path('verify', views.CheckLoginViewSet.as_view()),
    path('check_phone_number', views.CheckNumberLoginViewSet.as_view()),
    path('user_data', views.GetUserDataViewSet.as_view()),
    path('create_job/', views.JobCreateViewSet.as_view()),
    path('modify_company/', views.AddAndEditUserCompamyViewSet.as_view()),
    path('modify_job/', views.JobModifyViewSet.as_view()),
    path('edit_user/', views.EditUserProfileViewSet.as_view()),
    path('add_cv/', views.AddCVToUserViewSet.as_view()),
    path('send_cv/', views.SendCVJobViewSet.as_view()),
    path('get_cv', views.GetUserCVsViewSet.as_view()),
    path('check_company', views.IsCompanyInfoCompleteViewSet.as_view()),
    path('get_company_cv', views.GetCompanyCVViewSet.as_view()),
    path('edit_company_cv/', views.EditCompanyCVViewSet.as_view()),
    path('get_company_ads', views.GetCompanyAdsViewSet.as_view()),
    path('company_ad_demo/<str:slug>', views.CompanyAdDemoViewSet.as_view()),
]
