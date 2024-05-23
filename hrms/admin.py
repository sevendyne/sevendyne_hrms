from django.contrib import admin
from hrms.models import HrmsClient


class HrmsClientAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(HrmsClient, HrmsClientAdmin) 