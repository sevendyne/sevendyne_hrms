from django.contrib import admin
from main.models import Company, CompanyAccess

class CompanyAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Company, CompanyAdmin) 


class CompanyAccessAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(CompanyAccess, CompanyAccessAdmin) 