from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.main.models import BaseModel


CATEGORY_CHOICES = (
    ('Additions', "Additions"),
    ('Deductions',"Deductions")
)


class SalarySetting(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    da = models.DecimalField(_('DA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    hra = models.DecimalField(_('HRA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    pf_emp = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)    
    pf_org = models.DecimalField(_('Organization Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    esi_emp = models.DecimalField(_('ESI Employee(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    esi_org = models.DecimalField(_('ESI Organization(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    pf_fixed = models.DecimalField(_('If pf not in %, Total PF (in numbers)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    tds = models.DecimalField(_('TDS '),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    is_deleted = models.BooleanField(_('Is This Salary Settings Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False,null=True,blank=True)

    class Meta:
        verbose_name = _('Salary Settings')
        verbose_name_plural = _('Salary Settings')
        ordering = ['da']
    
    def __str__(self):
        return str(self.da)
    

class PayrollItem(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    name = models.CharField(_('Payroll Item Name'),max_length=255)
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES, default='Additions')
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

    class Meta:
        verbose_name = _('Payroll Item')
        verbose_name_plural = _('Payroll Items')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.category}"


class Salary(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})      
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    net_salary = models.DecimalField(_('Net Salary'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])    
    date = models.DateField()
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

    class Meta:
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')
        ordering = ['employee']

    def __str__(self):
        return f"{self.employee} - {self.net_salary}"


class SalaryDynamicField(models.Model):
    company = models.ForeignKey("main.Company", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})      
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})    
    salary = models.ForeignKey("payroll.Salary", on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    field_value = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    category = models.CharField(max_length=255)
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

    class Meta:
        verbose_name = _('SalaryDynamicField')
        verbose_name_plural = _('SalaryDynamicFields')
        ordering = ['employee']

    def __str__(self):
        return f"{self.field_name} - {self.field_value}"
    
