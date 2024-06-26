from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from main.models import BaseModel


LEAVE_STATUS = (
    ('Pending', "Pending"),
    ('Approved',"Approved"),
    ('Rejected',"Rejected")    
)

ATTENDANCE_CHOICES = {
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('half-day','Half')
}

GENDER_CHOICES = {
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other','Other')
}


class Department(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    name = models.CharField(_("Department Name"),max_length=125)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Designation(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    name = models.CharField(_("Designation Name"),max_length=255)#formset
    department = models.ForeignKey("employee.Department",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(_('Firstname'),max_length=125)
    lastname = models.CharField(_('Lastname'),max_length=125)
    gender = models.CharField(_('Gender'),choices=GENDER_CHOICES,max_length=125,null=True, blank=True)
    username = models.CharField(max_length=254)    
    password = models.CharField(max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone Number"),max_length=255)
    address = models.TextField(_("Address"),null=True, blank=True)
    # client_company = models.ForeignKey("client.Client",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) #client company foreign key
    department =  models.ForeignKey("employee.Department",verbose_name =_('Department'),on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    designation =  models.ForeignKey("employee.Designation",verbose_name =_('Role'),on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    joindate = models.DateField(_('Joining Date'),help_text='joining date',blank=True,null=True)    
    employeeid = models.CharField(_('Employee ID'),max_length=125)
    photo = models.ImageField(_("Photo"), upload_to='employee_photos/',null=True,blank=True)

    is_blocked = models.BooleanField(_('Is This Employee Blocked ?'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

   
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['firstname']
        unique_together = ('user','company', 'employeeid','email')

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        if self.lastname:
            full_name = f"{self.firstname} {self.lastname}"
        else:
            full_name = self.firstname
        return full_name
    
    def get_attendance(self,month,date):
        if AttendanceRegister.objects.filter(employee=self,date__month=month,date__day=date,is_deleted=False).exists():
            att = AttendanceRegister.objects.filter(employee=self,date__month=month,date__day=date,is_deleted=False)
            if att.filter(is_fn=True,is_an=True).exists():
                att.update(status = 'present')
                return True
            elif att.filter(is_fn=False,is_an=True).exists():
                att.update(status = 'half-day')
                return "AnHalf"
            elif att.filter(is_fn=True,is_an=False).exists():
                att.update(status = 'half-day')
                return "FnHalf"
            elif att.filter(is_fn=False,is_an=False).exists():
                att.update(status = 'absent')
                return False
            elif att.filter(is_attended=False).exists():
                att.update(status = 'absent')
                return False
            elif att.filter(is_attended=True).exists():
                att.update(status = 'present')
                return True            
            else:
                att.update(status = 'absent')
                return False
        else:
            return 'blank'
    

class LeaveType(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})   
    name = models.CharField(_("Leave Type"),max_length=255)
    days = models.PositiveIntegerField(_("Number of Days"),null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Leave Type')
        verbose_name_plural = _('Leave Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Leave(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})  
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    startdate = models.DateField(verbose_name=_('From'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_('To'), help_text='coming back on ...', null=True, blank=False)
    leavetype = models.ForeignKey("employee.LeaveType", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    reason = models.CharField(verbose_name=_('Leave Reason'), max_length=255, help_text='add additional information for leave', null=True, blank=True)
    leave_days = models.PositiveIntegerField(_("Number of Leave Days"))
    status = models.CharField(max_length=128, choices=LEAVE_STATUS, default='Pending') # pending, approved, rejected, cancelled
    is_approved = models.BooleanField(default=False) 
    is_rejected = models.BooleanField(default=False) 
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['leavetype'] 

    def __str__(self):
        return f"{self.employee} - {self.leavetype}"
    

class AttendanceRegister(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})  
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    status = models.CharField (max_length=15,choices=ATTENDANCE_CHOICES,default='absent')
    date = models.DateField()    

    is_attended = models.BooleanField(default=True)
    is_fn = models.BooleanField(default=True)
    is_an = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  

    class Meta:
        db_table = 'attendence_register'
        verbose_name = _('attendence register')
        verbose_name_plural = _('attendence registers')

    def __str__(self):
        return str(self.employee)
    

class Holiday(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})  
    name = models.CharField(_("Name"),max_length=125)
    date = models.DateField(_('Date'),help_text='due_date',blank=False,null=True)    
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'holiday'
        verbose_name = _('holiday')
        verbose_name_plural = _('holidays')
    
    def __str__(self):
        return self.name