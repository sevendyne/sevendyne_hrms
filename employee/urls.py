from django.urls import path, re_path
from employee import views

urlpatterns = [
    
    path('department/create/', views.create_department, name='create_department'),
    path("departments/", views.departments, name="departments"),
    re_path(r'^department/edit/(?P<pk>.*)/$', views.edit_department, name='edit_department'),
    re_path(r'^delete-department/(?P<pk>.*)/$', views.delete_department, name='delete_department'),    
    re_path(r'^department/(?P<pk>.*)/$', views.department, name='department'),
    
    path('designation/create/', views.create_designation, name='create_designation'),
    path("designations/", views.designations, name="designations"),
    re_path(r'^designation/edit/(?P<pk>.*)/$', views.edit_designation, name='edit_designation'),
    re_path(r'^delete-designation/(?P<pk>.*)/$', views.delete_designation, name='delete_designation'),    
    re_path(r'^designation/(?P<pk>.*)/$', views.designation, name='designation'),
    
    path('employee/create/', views.create_employee, name='create_employee'),
    path("employees/", views.employees, name="employees"),
    re_path(r'^employee/edit/(?P<pk>.*)/$', views.edit_employee, name='edit_employee'),
    re_path(r'^delete-employee/(?P<pk>.*)/$', views.delete_employee, name='delete_employee'),    
    re_path(r'^employee/(?P<pk>.*)/$', views.employee, name='employee'),
   
]

