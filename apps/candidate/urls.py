from django.urls import path, re_path
from apps.candidate import views

urlpatterns = [
    
    path('candidate/create/', views.create_candidate, name='create_candidate'),
    path("candidates/", views.candidates, name="candidates"),
    path("hrms-candidates/", views.hrms_candidates, name="hrms_candidates"),
    re_path(r'^candidate/edit/(?P<pk>.*)/$', views.edit_candidate, name='edit_candidate'),
    re_path(r'^delete-candidate/(?P<pk>.*)/$', views.delete_candidate, name='delete_candidate'),
    path('candidate/delete-selected/', views.delete_selected_candidates, name='delete_selected_hrms_candidates'),
    re_path(r'^candidate/(?P<pk>.*)/$', views.candidate, name='candidate'),   
    path('apply/', views.candidate_application, name='candidate_application'),

    path('enroll/',views.create_intern,name='create_intern'),
    path("interns/", views.interns, name="interns"),
    re_path(r'^intern/(?P<pk>.*)/$', views.intern, name='intern'),   
]

