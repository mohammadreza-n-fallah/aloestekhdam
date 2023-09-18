from django.urls import path
from . import views


urlpatterns = [
    path ('list' , views.JobListViewSet.as_view()),
    path ('get/<str:slug>' , views.JobRetrieveViewSet.as_view()),
    path ('search' , views.JobSearchViewSet.as_view()),
]