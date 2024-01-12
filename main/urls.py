from django.urls import path, re_path
from main import views
from main.autocomplete_registery import StateAutocomplete

urlpatterns = [

    path("hrms/dashboard/", views.hrms_dashboard, name="hrms_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),

	# path('state-autocomplete/',StateAutocomplete.as_view(),name='state_autocomplete'),
    # path('get_states/', views.get_states, name='get_states'),
	path('company/create/', views.create_company, name='create_company'),
    path('companies/', views.companies, name='companies'),
    re_path(r'^company/edit/(?P<pk>.*)/$', views.edit_company, name='edit_company'),
    re_path(r'^company/(?P<pk>.*)/$', views.company, name='company'),
    re_path(r'^delete-company/(?P<pk>.*)/$', views.delete_company, name='delete_company'),
    path('company/delete-selected/', views.delete_selected_companies, name='delete_selected_companies')

]

