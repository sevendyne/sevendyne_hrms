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
    
    path('leave_type/create/', views.create_leave_type, name='create_leave_type'),
    path("leave_types/", views.leave_types, name="leave_types"),
    re_path(r'^leave_type/edit/(?P<pk>.*)/$', views.edit_leave_type, name='edit_leave_type'),
    re_path(r'^delete-leave_type/(?P<pk>.*)/$', views.delete_leave_type, name='delete_leave_type'),    
    re_path(r'^leave_type/(?P<pk>.*)/$', views.leave_type, name='leave_type'),
    
    path('leave/create/', views.create_leave, name='create_leave'),
    path("leaves/", views.leaves, name="leaves"),
    # re_path(r'^delete-leave/(?P<pk>.*)/$', views.delete_leave, name='delete_leave'),    
    # re_path(r'^leave/(?P<pk>.*)/$', views.leave, name='leave'),
   
    path('ajax_load_remaining_days', views.ajax_load_remaining_days, name='ajax_load_remaining_days'),
    
    path('leave-approval/create/', views.create_leave, name='create_leave'),
    path("leave-approvals/", views.leave_approvals, name="leave_approvals"),
    re_path(r'^leave/edit/(?P<pk>.*)/$', views.edit_leave, name='edit_leave'),
    # re_path(r'^delete-leave/(?P<pk>.*)/$', views.delete_leave, name='delete_leave'),    
    re_path(r'^leave-approval/(?P<pk>.*)/$', views.leave_approval, name='leave_approval'),
   
]

