from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.main import views as general_views
from apps.main.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", general_views.robots_txt, name="robots_txt"),
    path("admin/", admin.site.urls),
    path("app/", include(("apps.user.urls", "user"), namespace="user")),
    path("", general_views.job_portal, name="job_portal"),
    path("app/hrms/dashboard/", general_views.hrms_dashboard, name="hrms_dashboard"),
    path("", include(("apps.main.urls", "main"), namespace="main")),
    path("app/hrms/", include(("apps.hrms.urls", "hrms"), namespace="hrms")),
    path(
        "app/candidate/",
        include(("apps.candidate.urls", "candidate"), namespace="candidate"),
    ),
    path(
        "app/employee/",
        include(("apps.employee.urls", "employee"), namespace="employee"),
    ),
    path("app/client/", include(("apps.client.urls", "client"), namespace="client")),
    path("app/job/", include(("apps.job.urls", "job"), namespace="job")),
    path("app/payroll/", include(("apps.payroll.urls", "payroll"), namespace="payroll")),
    path("app/asset/", include(("apps.asset.urls", "asset"), namespace="asset")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.main.views.custom_404"
handler500 = "apps.main.views.custom_500"
