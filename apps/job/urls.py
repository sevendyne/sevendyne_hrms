from django.urls import path, re_path
from . import views

app_name = "job"

urlpatterns = [
    path('job/create/', views.create_job, name='create_job'),
    path('jobs/', views.jobs, name="jobs"),
    path('all-jobs/', views.all_jobs, name="all_jobs"),
    re_path(r'^job/edit/(?P<pk>.*)/$', views.edit_job, name='edit_job'),
    re_path(r'^delete-job/(?P<pk>.*)/$', views.delete_job, name='delete_job'),  
    
    re_path(r'^job/view/(?P<pk>.*)/$', views.job_view, name='job_view'),  
    re_path(r'^job/(?P<pk>.*)/$', views.job, name='job'),

    re_path(r'^candidate-job/create/(?P<pk>.*)/$', views.create_candidate_job, name='create_candidate_job'),
    path('candidate-jobs/', views.candidate_jobs, name="candidate_jobs"),
    re_path(r'^candidate-job/edit/(?P<pk>.*)/$', views.edit_candidate_job, name='edit_candidate_job'),
    re_path(r'^delete-candidate-job/(?P<pk>.*)/$', views.delete_candidate_job, name='delete_candidate_job'),
    re_path(r'^candidate-job/(?P<pk>.*)/$', views.candidate_job, name='candidate_job'),

    re_path(r'^candidate-interview/create/(?P<pk>.*)/$', views.create_candidate_interview, name='create_candidate_interview'),
    path('candidate-interviews/', views.candidate_interviews, name="candidate_interviews"),
    re_path(r'^candidate-interview/edit/(?P<pk>.*)/$', views.edit_candidate_interview, name='edit_candidate_interview'),
    re_path(r'^candidate-interview/update/(?P<pk>.*)/$', views.update_candidate_interview_status, name='update_candidate_interview_status'),
    re_path(r'^delete-candidate-interview/(?P<pk>.*)/$', views.delete_candidate_interview, name='delete_candidate_interview'),
    re_path(r'^candidate-interview/(?P<pk>.*)/$', views.candidate_interview, name='candidate_interview'),

] 