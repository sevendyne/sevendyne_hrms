from decimal import Decimal
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator,MinValueValidator

from main.models import BaseModel


CATEGORY_CHOICES = (
    ('Additions', "Additions"),
    ('Deductions',"Deductions")
)

# Create your models here.
class SalarySettings(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    da = models.DecimalField(_('DA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    hra = models.DecimalField(_('HRA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    pf_emp = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])    
    pf_org = models.DecimalField(_('Organization Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    esi_emp = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    esi_org = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    tds = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    is_deleted = models.BooleanField(_('Is This Salary Settings Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

   
    class Meta:
        verbose_name = _('Salary Settings')
        verbose_name_plural = _('Salary Settings')
        ordering = ['da']
    
    def __str__(self):
        return self.da
    
# in forms.py , widgets, 'category': Select(attrs={'class': 'required form-control selectpicker'}),   
# class PayrollItem(BaseModel):  
#     company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     name = models.CharField(_('Payroll Item Name'),max_length=255)
#     category = models.CharField(max_length=128, choices=CATEGORY_CHOICES, default='Additions')
#     is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

   
#     class Meta:
#         verbose_name = _('Payroll Item')
#         verbose_name_plural = _('Payroll Items')
#         ordering = ['name']

#     def __str__(self):
#         return self.name

# subtract leave days salary also to get net salary
# class Salary(BaseModel):  
#     company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     payroll_item = models.ForeignKey("payroll.PayrollItem",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
#     is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)


#     class Meta:
#         verbose_name = _('Salary')
#         verbose_name_plural = _('Salary')
#         ordering = ['name']

#     def __str__(self):
#         return self.name

#     @property
#     def net_salary(self):
#         if self.lastname:
#             full_name = f"{self.firstname} {self.lastname}"
#         else:
#             full_name = self.firstname
#         return full_name
    

#print payslip
