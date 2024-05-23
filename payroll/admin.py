from django.contrib import admin
from payroll.models import PayrollItem, Salary, SalaryDynamicField, SalarySetting


class SalarySettingAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(SalarySetting, SalarySettingAdmin) 


class PayrollItemAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(PayrollItem, PayrollItemAdmin) 


class SalaryAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Salary, SalaryAdmin) 


class SalaryDynamicFieldAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(SalaryDynamicField, SalaryDynamicFieldAdmin) 