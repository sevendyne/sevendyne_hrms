from user import views
from django.urls import path

app_name = "user"

urlpatterns = [
    path("login/",views.user_login,name="user_login"),
    path("register/",views.register,name="register"),
    path("logout/", views.user_logout, name="user_logout"),
]