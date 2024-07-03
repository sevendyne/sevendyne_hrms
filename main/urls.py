from django.urls import path, re_path
from main import views
from main.autocomplete_registery import StateAutocomplete

urlpatterns = [
    path("", views.job_portal, name="job_portal"),
    path("jobs/", views.job_list, name="job_list"),
    path('about/',views.about,name='about'),
    path('terms_and_conditions/',views.terms_and_conditions,name='terms_and_conditions'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
    path('portfolio-home/',views.portfolios_home,name='portfolios_home'),
    path('home/hrms/',views.home_hrms,name='home_hrms'),

    path('get_states/', views.get_states, name='get_states'),

    path('portfolio/create/', views.create_portfolio, name='create_portfolio'),
    path('portfolios/', views.portfolios, name="portfolios"),
    re_path(r'^portfolio/edit/(?P<pk>.*)/$', views.edit_portfolio, name='edit_portfolio'),
    re_path(r'^portfolio/(?P<pk>.*)/$', views.portfolio, name='portfolio'),
    re_path(r'^delete-portfolio/(?P<pk>.*)/$', views.delete_portfolio, name='delete_portfolio'),

    path("hrms/home/", views.home_hrms, name="home_hrms"),
    path("hrms/dashboard/", views.hrms_dashboard, name="hrms_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),

	path('company/create/', views.create_company, name='create_company'),
    path('companies/', views.companies, name="companies"),
    re_path(r'^company/edit/(?P<pk>.*)/$', views.edit_company, name='edit_company'),
    re_path(r'^company/(?P<pk>.*)/$', views.company, name='company'),

    path('email-setting/create/', views.create_email_setting, name='create_email_setting'),
    path("email-settings/", views.email_settings, name="email_settings"),
    re_path(r'^email-setting/edit/(?P<pk>.*)/$', views.edit_email_setting, name='edit_email_setting'),
    re_path(r'^delete-email-setting/(?P<pk>.*)/$', views.delete_email_setting, name='delete_email_setting'),    
    re_path(r'^email-setting/(?P<pk>.*)/$', views.email_setting, name='email_setting')
]

