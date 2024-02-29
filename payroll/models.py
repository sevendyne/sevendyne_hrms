import datetime
from datetime import date
from decimal import Decimal
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator,MinValueValidator
from employee.models import Employee

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
    net_salary = models.DecimalField(_('Net Salary'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    # basic_salary = models.DecimalField(_('Basic Salary'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)


    class Meta:
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')
        ordering = ['employee']

    def __str__(self):
        return str(self.net_salary)
    
    
#print payslip

class SalaryData(models.Model):
    company = models.ForeignKey("main.Company", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})      
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    # salary = models.ForeignKey("payroll.Salary", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    net_salary = models.DecimalField(_('Net Salary'),default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    date = models.DateField(_("Date"), default=date.today)
    is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if not self.pk:
        self.dynamic_field_names = set()

        
    def get_dynamic_fields(self):
        return [field for field in self._meta.get_fields() if not field.name.startswith('_') and field.name in self.dynamic_field_names]

    
    @classmethod
    def create_dynamic_fields(cls, company, data):
        # Retrieve the Employee instance corresponding to the employee_id
        employee_id = data.get('employee')
        employee = Employee.objects.get(id=employee_id)

        # Check if a SalaryData instance already exists for the employee and company
        existing_salary_data = SalaryData.objects.filter(company=company, employee=employee, is_deleted=False).first()

        if existing_salary_data:
            # If an instance already exists, update its dynamic fields and return it
            instance = existing_salary_data
        else:
            # If no instance exists, create a new one
            instance = cls(company=company, employee=employee)

        # Set the dynamic fields and save the instance
        for key, value in data.items():
            if key not in ["employee", "net_salary"]:
                field_name = key.split('[')[-1][:-1]  # Extracts field name from "formData[Field_Name]"
                setattr(instance, field_name, value)
                instance.dynamic_field_names.add(field_name)
                print("instance.dynamic_field_names",instance.dynamic_field_names)
        # Set the net_salary attribute of the instance
        net_salary = data.get('net_salary')
        instance.net_salary = net_salary

        # Save the instance to the database
        instance.save()

        return instance

    # @classmethod
    # def create_dynamic_fields(cls, company, data):
    #     instance = cls()
    #     print("instance",instance)
    #     # valid_field_names = set()
    #     # print("valid field names in set()",valid_field_names)
    #     for key, value in data.items():
    #         # Skip keys named "employee" and "net_salary"
    #         if key not in ["employee", "net_salary"]:
    #             # Extract the field name from the key
    #             field_name = key.split('[')[-1][:-1]  # Extracts field name from "formData[Field_Name]"
                
    #             setattr(instance, field_name, value)
    #             instance.dynamic_field_names.add(field_name)
    #             print("instance.dynamic_field_names",instance.dynamic_field_names)
                
    #         # valid_field_names.add(field_name)
    #         # print("valid field names after",valid_field_names)
    #         # if field_name in valid_field_names:
    #         #     print(f"Setting attribute: {field_name} -> {value}")
    #         #     setattr(instance, field_name, value)
    #         # else:
    #         #     print(f"Ignoring attribute: {key} (not a valid field name)")            
    #     # Retrieve the Employee instance corresponding to the employee_id
    #     employee_id = data.get('employee')
    #     employee = Employee.objects.get(id=employee_id)
    #     instance.employee = employee
    #     instance.company=company
    #     net_salary = data.get('net_salary')
    #     instance.salary=net_salary
    #     instance.save()  
    #     # Print the instance along with its attributes
    #     print("Instance with attributes:", instance.__dict__)
    #     # print("instance")
    #     return instance
    
    def __str__(self):
        return f"SalaryData object (ID: {self.pk})"

# class PaySlip(models.Model):
#     salary = models.ForeignKey("payroll.Salary", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
#     payroll_items = models.ManyToManyField(PayrollItem)
#     date = models.DateField(_("Date"), default=date.today)
#     is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

#     class Meta:
#         verbose_name = _('Payslip')
#         verbose_name_plural = _('Payslips')

#     def __str__(self):
#         return f"{self.employee} - {self.date}"
    
# class PaySlipItem(models.Model):
#     payslip = models.ForeignKey(PaySlip, on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
#     payroll_item = models.ForeignKey(PayrollItem, on_delete=models.CASCADE)
#     value = models.DecimalField(max_digits=15, decimal_places=2)
#     category = models.CharField(max_length=128)
#     is_deleted = models.BooleanField(_('Is This Employee Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)

#     class Meta:
#         verbose_name = _('PaySlip Item')
#         verbose_name_plural = _('PaySlip Items')

#     def __str__(self):
#         return f"{self.payslip.employee} - {self.payroll_item.name}"