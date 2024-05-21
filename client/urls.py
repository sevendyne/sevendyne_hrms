from django.urls import path, re_path
from client import views

urlpatterns = [    
    path('project/create/', views.create_client, name='create_client'),
    path("projects/", views.clients, name="clients"),
    path("projects-list/", views.clients_list, name="clients_list"),
    re_path(r'^project/edit/(?P<pk>.*)/$', views.edit_client, name='edit_client'),
    re_path(r'^delete-project/(?P<pk>.*)/$', views.delete_client, name='delete_client'),    
    re_path(r'^project/(?P<pk>.*)/$', views.client, name='client')        
]

