from user import views
from django.urls import path

app_name = "user"

urlpatterns = [
    path("",views.user_login,name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
]