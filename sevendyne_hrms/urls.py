from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from main import views as general_views
from sevendyne_hrms import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path('app/',include(('user.urls','user'),namespace='user')),
    path('',general_views.job_portal,name='job_portal'),
    path('app/hrms/dashboard/',general_views.hrms_dashboard,name='hrms_dashboard'),
    path('app/sevendyne/dashboard/',general_views.admin_dashboard,name='sevendyne_dashboard'),
    path('app/main/',include(('main.urls','main'),namespace='main')),
    path('app/hrms/',include(('hrms.urls','hrms'),namespace='hrms')),
    path('app/candidate/',include(('candidate.urls','candidate'),namespace='candidate')),
    path('app/employee/',include(('employee.urls','employee'),namespace='employee')),
    path('app/client/',include(('client.urls','client'),namespace='client')),
    path('app/job/',include(('job.urls','job'),namespace='job')),
    path('app/payroll/',include(('payroll.urls','payroll'),namespace='payroll')),
    path('app/task-board/',include(('taskboard.urls','taskboard'),namespace='taskboard')),
    path('app/asset/',include(('asset.urls','asset'),namespace='asset'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

