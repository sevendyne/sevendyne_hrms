from django.urls import path, re_path
from main import views
from main.autocomplete_registery import StateAutocomplete

urlpatterns = [

    path("", views.home_hrms, name="home_hrms"),
    path("hrms/dashboard/", views.hrms_dashboard, name="hrms_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),

	# path('state-autocomplete/',StateAutocomplete.as_view(),name='state_autocomplete'),
    path('get-states/', views.get_states, name='get_states'),
	path('company/create/', views.create_company, name='create_company'),
    path('companies/', views.companies, name="companies"),
    re_path(r'^company/edit/(?P<pk>.*)/$', views.edit_company, name='edit_company'),
    re_path(r'^company/(?P<pk>.*)/$', views.company, name='company'),
   
    path('portfolio/create/', views.create_portfolio, name='create_portfolio'),
    path('portfolios/', views.portfolios, name="portfolios"),
    re_path(r'^portfolio/edit/(?P<pk>.*)/$', views.edit_portfolio, name='edit_portfolio'),
    re_path(r'^portfolio/(?P<pk>.*)/$', views.portfolio, name='portfolio'),
    re_path(r'^delete-portfolio/(?P<pk>.*)/$', views.delete_portfolio, name='delete_portfolio')
   
]

