import datetime
from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(_('Firstname'),max_length=125,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,blank=False)
    username = models.CharField(max_length=254)    
    password = models.CharField(max_length=100)
    email = models.EmailField(_("Email"),unique=True)
    phone = PhoneNumberField(_("Phone Number"))
    address = models.TextField(_("Address"),null=True, blank=True)
    client_company = models.ForeignKey("client.Client",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) #client company foreign key
    department =  models.ForeignKey("employee.Department",verbose_name =_('Department'),on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    designation =  models.ForeignKey("employee.Designation",verbose_name =_('Role'),on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    joindate = models.DateField(_('Joining Date'),help_text='joining date',blank=False,null=True)    
    employeeid = models.CharField(_('Employee ID'),max_length=125,unique=True,null=True,blank=True)

    is_blocked = models.BooleanField(_('Is This Employee Blocked ?'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

   
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['firstname']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        if self.lastname:
            full_name = f"{self.firstname} {self.lastname}"
        else:
            full_name = self.firstname
        return full_name
    

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



# class Leave(models.Model):
# 	user/employee = models.ForeignKey(User/employee,on_delete=models.CASCADE,default=1)
# 	startdate = models.DateField(verbose_name=_('Start Date'),help_text='leave start date is on ..',null=True,blank=False)
# 	enddate = models.DateField(verbose_name=_('End Date'),help_text='coming back on ...',null=True,blank=False)
# 	leavetype = models.CharField(choices=LEAVE_TYPE,max_length=25,default=SICK,null=True,blank=False)
# 	reason = models.CharField(verbose_name=_('Reason for Leave'),max_length=255,help_text='add additional information for leave',null=True,blank=True)
# 	defaultdays = models.PositiveIntegerField(verbose_name=_('Leave days per year counter'),default=DAYS,null=True,blank=True)


# 	# hrcomments = models.ForeignKey('CommentLeave') #hide

# 	status = models.CharField(max_length=12,default='pending') #pending,approved,rejected,cancelled
# 	is_approved = models.BooleanField(default=False) #hide
# 	is_deleted = models.BooleanField(default=False)

# 	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
# 	created = models.DateTimeField(auto_now=False, auto_now_add=True)


	
# 	class Meta:
# 		verbose_name = _('Leave')
# 		verbose_name_plural = _('Leaves')
# 		ordering = ['-created'] #recent objects



# 	def __str__(self):
# 		return ('{0} - {1}'.format(self.leavetype,self.user))




# 	@property
# 	def pretty_leave(self):
# 		'''
# 		i don't like the __str__ of leave object - this is a pretty one :-)
# 		'''
# 		leave = self.leavetype
# 		user = self.user
# 		employee = user.employee_set.first().get_full_name
# 		return ('{0} - {1}'.format(employee,leave))



# 	@property
# 	def leave_days(self):
# 		days_count = ''
# 		startdate = self.startdate
# 		enddate = self.enddate
# 		if startdate > enddate:
# 			return
# 		dates = (enddate - startdate)
# 		return dates.days



# 	@property
# 	def leave_approved(self):
# 		return self.is_approved == True




# 	@property
# 	def approve_leave(self):
# 		if not self.is_approved:
# 			self.is_approved = True
# 			self.status = 'approved'
# 			self.save()




# 	@property
# 	def unapprove_leave(self):
# 		if self.is_approved:
# 			self.is_approved = False
# 			self.status = 'pending'
# 			self.save()



# 	@property
# 	def leaves_cancel(self):
# 		if self.is_approved or not self.is_approved:
# 			self.is_approved = False
# 			self.status = 'cancelled'
# 			self.save()



# 	# def uncancel_leave(self):
# 	# 	if  self.is_approved or not self.is_approved:
# 	# 		self.is_approved = False
# 	# 		self.status = 'pending'
# 	# 		self.save()



# 	@property
# 	def reject_leave(self):
# 		if self.is_approved or not self.is_approved:
# 			self.is_approved = False
# 			self.status = 'rejected'
# 			self.save()



# 	@property
# 	def is_rejected(self):
# 		return self.status == 'rejected'

