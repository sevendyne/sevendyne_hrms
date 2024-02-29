from django.urls import path, re_path
from payroll import views

urlpatterns = [

    # path('ajax_load_da', views.ajax_load_da, name='ajax_load_da'),
    path('ajax_load_salary_components', views.ajax_load_salary_components, name='ajax_load_salary_components'),
        
    path('salary-setting/create/', views.create_salary_setting, name='create_salary_setting'),
    path("salary-settings/", views.salary_settings, name="salary_settings"),
    re_path(r'^salary-setting/edit/(?P<pk>.*)/$', views.edit_salary_setting, name='edit_salary_setting'),
    re_path(r'^delete-salary-setting/(?P<pk>.*)/$', views.delete_salary_setting, name='delete_salary_setting'),    
    re_path(r'^salary-setting/(?P<pk>.*)/$', views.salary_setting, name='salary_setting'),
    
    path('payroll-item/create/', views.create_payroll_item, name='create_payroll_item'),
    path("payroll-items/", views.payroll_items, name="payroll_items"),
    re_path(r'^payroll-item/edit/(?P<pk>.*)/$', views.edit_payroll_item, name='edit_payroll_item'),
    re_path(r'^delete-payroll-item/(?P<pk>.*)/$', views.delete_payroll_item, name='delete_payroll_item'),    
    re_path(r'^payroll-item/(?P<pk>.*)/$', views.payroll_item, name='payroll_item'),

    path('salary/create/', views.create_salary, name='create_salary'),
    path("salaries/", views.salaries, name="salaries"),
    re_path(r'^salary/edit/(?P<pk>.*)/$', views.edit_salary, name='edit_salary'),
    re_path(r'^delete-salary/(?P<pk>.*)/$', views.delete_salary, name='delete_salary'),    
    re_path(r'^salary/(?P<pk>.*)/$', views.salary, name='salary'),
    
    path('salary-data/create/', views.process_salary_data, name='process_salary_data'),
    # path('payslip/', views.payslip, name='payslip'),
    re_path(r'^payslip/(?P<pk>.*)/$', views.payslip, name='payslip'),

]