from django.urls import path, re_path
from asset import views

urlpatterns = [    
    path('asset/create/', views.create_asset, name='create_asset'),
    path("assets/", views.assets, name="assets"),
    re_path(r'^asset/edit/(?P<pk>.*)/$', views.edit_asset, name='edit_asset'),
    re_path(r'^delete-asset/(?P<pk>.*)/$', views.delete_asset, name='delete_asset'),    
    re_path(r'^asset/(?P<pk>.*)/$', views.asset, name='asset')
]

