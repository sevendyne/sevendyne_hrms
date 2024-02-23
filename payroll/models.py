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


class SalarySetting(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    da = models.DecimalField(_('DA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    hra = models.DecimalField(_('HRA(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    pf_emp = models.DecimalField(_('Employee Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)    
    pf_org = models.DecimalField(_('Organization Share(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    esi_emp = models.DecimalField(_('ESI Employee(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    esi_org = models.DecimalField(_('ESI Organization(%)'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
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
        return str(self.name)

# subtract leave days salary also to get net salary. calculate net salary
class Salary(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})      
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    payroll_item = models.ForeignKey("payroll.PayrollItem",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    net_salary = models.DecimalField(_('Net Salary'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)


    class Meta:
        verbose_name = _('Salary')
        verbose_name_plural = _('Salary')
        ordering = ['payroll_item']

    def __str__(self):
        return self.get_net_salary
    
    @property
    def get_net_salary(self):
        total_additions = 0
        total_deductions = 0
        
        # Assuming payroll_item has a field named value that holds the value for each payroll item
        for item in self.payroll_item.all():
            if item.category == 'Additions':
                total_additions += item.value
            elif item.category == 'Deductions':
                total_deductions += item.value
        
        basic_salary = self.employee.basic_salary  # Assuming employee has a field named basic_salary
        
        net_salary = basic_salary + total_additions - total_deductions
        return net_salary

    # @property
    # def net_salary(self):
    #     net_salary=0
    #     if self.payroll_item.category=="Additions":
    #         net_salary+=self.payroll_item
    #         pass
    #     else:
    #         net_salary-=self.payroll_item
    #     return net_salary
    
    # @property
    # def calculate_da(self):
    #     # Fetch SalarySetting for the company
    #     salary_setting = SalarySetting.objects.get(company=self.company)

    #     # Calculate DA based on base salary and DA percentage
    #     da_amount = self.base_salary * (salary_setting.da / 100)
    #     return da_amount
    

#print payslip
