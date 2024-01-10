from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from main import views as general_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include(('user.urls','user'),namespace='user')),
    # path('',general_views.app,name='app'),
    path('app/hrms/dashboard/',general_views.hrms_dashboard,name='hrms_dashboard'),
    path('app/sevendyne/dashboard/',general_views.sevendyne_dashboard,name='sevendyne_dashboard'),
    path('app/main/',include(('main.urls','main'),namespace='main')),
    path('app/hrms/',include(('hrms.urls','hrms'),namespace='hrms')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

