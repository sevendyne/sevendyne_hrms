from . import views
from django.urls import path, re_path

app_name = "hrms"

urlpatterns = [
    path("client/create/", views.create_hrms_client, name="create_hrms_client"),
    path("clients/", views.hrms_clients, name="hrms_clients"),
    re_path(r'^hrms_client/edit/(?P<pk>.*)/$', views.edit_hrms_client, name='edit_hrms_client'),    
    re_path(r'^delete-hrms_client/(?P<pk>.*)/$', views.delete_hrms_client, name='delete_hrms_client'),
    path('hrms_client/delete-selected/', views.delete_selected_hrms_clients, name='delete_selected_hrms_clients'),
    re_path(r'^hrms_client/(?P<pk>.*)/$', views.hrms_client, name='hrms_client'),
]