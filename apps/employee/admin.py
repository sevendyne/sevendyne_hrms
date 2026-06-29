from django.contrib import admin
from apps.employee.models import AttendanceRegister, Department, Designation, Employee, Holiday, Leave, LeaveType


class DepartmentAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Department, DepartmentAdmin) 


class DesignationAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Designation, DesignationAdmin) 


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Employee, EmployeeAdmin) 


class LeaveTypeAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(LeaveType, LeaveTypeAdmin) 


class LeaveAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Leave, LeaveAdmin) 


class AttendanceRegisterAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(AttendanceRegister, AttendanceRegisterAdmin) 


class HolidayAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Holiday, HolidayAdmin) 