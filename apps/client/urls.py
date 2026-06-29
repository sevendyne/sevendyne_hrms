from django.urls import path, re_path
from apps.client import views

urlpatterns = [    
    path('client/create/', views.create_client, name='create_client'),
    path("clients/", views.clients, name="clients"),
    path("clients-list/", views.clients_list, name="clients_list"),
    re_path(r'^client/edit/(?P<pk>.*)/$', views.edit_client, name='edit_client'),
    re_path(r'^delete-client/(?P<pk>.*)/$', views.delete_client, name='delete_client'),    
    re_path(r'^client/(?P<pk>.*)/$', views.client, name='client')        
]

