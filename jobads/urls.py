from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoryApiView.as_view()),
    path('list', views.JobListViewSet.as_view()),
    path('get/<str:slug>', views.JobRetrieveViewSet.as_view()),
    path('search', views.JobSearchViewSet.as_view()),
    path('states', views.GetStateViewSet.as_view()),
    path('related_jobs', views.GetRelatedJobsViewSet.as_view()),
    path('get_income', views.GetJobIncomeViewSet.as_view()),
    path('get_time', views.GetJobTimeViewSet.as_view()),
    path('latest_jobs', views.GetLatestJobsViewSet.as_view()),
]
