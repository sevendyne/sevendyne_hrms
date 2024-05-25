import base64
import calendar
from num2words import num2words
from payroll.tasks import send_mail_payslip
from weasyprint import HTML
from xhtml2pdf import pisa

import json
import datetime
from io import BytesIO
from decimal import Decimal, InvalidOperation

from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from sevendyne_hrms import settings
from django.utils import timezone

from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_employee_dashboard_permission, has_hrms_permission
from payroll.models import  CATEGORY_CHOICES, PayrollItem, Salary, SalaryDynamicField, SalarySetting
from payroll.forms import PayrollItemForm, SalaryForm, SalarySettingForm
from employee.models import AttendanceRegister, Employee, Holiday


def get_last_payslip(request):
    if request.method == 'GET' and 'employee_id' in request.GET:
        employee_id = request.GET.get('employee_id')
        # Fetch the last created payslip for the employee
        try:
            last_payslip = Salary.objects.filter(employee_id=employee_id, is_deleted=False).order_by('-date').first()
            # If there's no payslip found for the employee, return an error response
            if not last_payslip:
                return JsonResponse({'error': 'No payslip found for the selected employee'}, status=404)
            
            # Fetch all salary dynamic fields related to the last payslip
            additions_fields = SalaryDynamicField.objects.filter(salary=last_payslip, category='Additions', is_deleted=False)
            deductions_fields = SalaryDynamicField.objects.filter(salary=last_payslip, category='Deductions', is_deleted=False)
            
            # Calculate total deductions
            total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
            # Get today's date
            today_date = datetime.date.today()
            
            # Prepare the data to send back to the client-side
            payslip_data = {
                'basic_salary': last_payslip.net_salary,  # Assuming 'net_salary' is considered as basic salary
                'net_salary': last_payslip.net_salary,
                'date': today_date,
                'additions_fields': list(additions_fields.values()),  # Convert QuerySet to list of dictionaries
                'deductions_fields': list(deductions_fields.values()),  # Convert QuerySet to list of dictionaries
                'total_deductions': total_deductions,
                # Include other relevant fields here
            }
            return JsonResponse(payslip_data)
        except Salary.DoesNotExist:
            return JsonResponse({'error': 'No payslip found for the selected employee'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method or missing employee_id parameter'}, status=400)


def ajax_load_salary_components(request):
    basic_salary = float(request.GET.get('basic_salary', 0))
    company=get_current_company(request)
    salary_settings = SalarySetting.objects.filter(company=company)
    salary_setting = salary_settings.first()
    # Calculate other salary components based on the basic salary
    da = float(basic_salary) * (float(salary_setting.da) / 100)
    hra = float(basic_salary) * (float(salary_setting.hra) / 100)
    esi = float(basic_salary) * (float(salary_setting.esi_emp+salary_setting.esi_org) / 100)
    pf = float(basic_salary) * (float(salary_setting.pf_emp+salary_setting.pf_org) / 100)
    tds = float(basic_salary) * (float(salary_setting.tds) / 100)   
    data = {
        'da': da,
        'hra': hra,
        'esi': esi,
        'pf': pf,
        'tds': tds
    }
    context = {
        'data':data
    }
    return render(request,'payroll/ajax_load_salary_components.html',context)


def fetch_total_working_days(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    total_working_days = Holiday.total_working_days_in_month(int(year), int(month))
    print("total_working_days",total_working_days)
    return JsonResponse({'total_working_days': total_working_days})

    
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_salary_setting(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = SalarySettingForm(request.POST)
        if form.is_valid():
            da = form.cleaned_data['da']
            hra = form.cleaned_data['hra']
            pf_emp = form.cleaned_data['pf_emp']
            pf_org = form.cleaned_data['pf_org']
            esi_emp = form.cleaned_data['esi_emp']
            esi_org = form.cleaned_data['esi_org']
            tds = form.cleaned_data['tds']            
            auto_id = get_auto_id(SalarySetting)
            a_id = get_a_id(SalarySetting,request)
            company =current_company
            creator = request.user
            updator = request.user
            if not SalarySetting.objects.filter(da=da,hra=hra,company=current_company,is_deleted=False).exists():
                SalarySetting(                    
                    da = da,
                    hra = hra,
                    pf_emp = pf_emp,
                    pf_org = pf_org,
                    esi_emp = esi_emp,
                    esi_org = esi_org,
                    tds = tds,                    
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Salary Setting created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('payroll:salaries_settings')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Salary Setting already exists",                        
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = SalarySettingForm()
        context = {
            "title": "Create Salary Setting",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'payroll/salary-settings.html', context)
    

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def salary_settings(request):
    current_company = get_current_company(request)
    salary_settings = SalarySetting.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(salary_settings,1000000000000)
    page_number = request.GET.get('page')
    salary_settings = paginator.get_page(page_number)
    context = {
        'salary_settings': salary_settings,
        "title": 'Salary Settings' 
    }
    return render(request, "payroll/salary-setting-list.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_salary_setting(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(SalarySetting.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = SalarySettingForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Salary Setting updated successfully.",                
                "redirect_url": reverse('payroll:salary_settings')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
                "message": str(message),
                "title": "Form validation error"  
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = SalarySettingForm(instance=instance)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Salary Setting ",            
            "redirect": "true",
            "url": reverse('payroll:edit_salarysetting', kwargs={'pk': instance.pk})
        }
        return render(request, 'payroll/salary-settings.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def salary_setting(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(SalarySetting.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Salary Setting'
    }
    return render(request, "payroll/salary-settings.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_salary_setting(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(SalarySetting.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    SalarySetting.objects.filter(pk=pk).update(is_deleted=True)
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Salary Setting Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('payroll:salary_settings')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

#payroll crud starts here
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_payroll_item(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = PayrollItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            auto_id = get_auto_id(PayrollItem)
            a_id = get_a_id(PayrollItem,request)
            company =current_company
            creator = request.user
            updator = request.user
            if not PayrollItem.objects.filter(name=name,category=category,company=current_company,is_deleted=False).exists():
                PayrollItem(                    
                    name = name,
                    category = category,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Payroll Item created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('payroll:payroll_items')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Payroll Item already exists",                        
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = PayrollItemForm()
        context = {
            "title": "Create Payroll Item",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'payroll/payroll-items.html', context)
    

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def payroll_items(request):
    current_company = get_current_company(request)
    payroll_items = PayrollItem.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(payroll_items,1000000000000)
    page_number = request.GET.get('page')
    payroll_items = paginator.get_page(page_number)
    context = {
        'payroll_items': payroll_items,
        "title": 'Payroll Items' ,
        'category_choices': CATEGORY_CHOICES      
    }
    return render(request, "payroll/payroll-items.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_payroll_item(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(PayrollItem.objects.filter(pk=pk,company=current_company, is_deleted=False))        
    if request.method == "POST":
        form = PayrollItemForm(request.POST, instance=instance)
        if form.is_valid():
            updated_payroll_item = form.save(commit=False)
            updated_payroll_item.updator = request.user
            updated_payroll_item.date_updated = datetime.datetime.now()
            updated_payroll_item.save()
            # Retrieve associated SalaryDynamicField instances
            salary_dynamic_fields = SalaryDynamicField.objects.filter(
                company=current_company,
                field_name=instance.name,  # Assuming name field in PayrollItem represents the field name in SalaryDynamicField
                is_deleted=False
            )
            # Update the field_name for each SalaryDynamicField instance
            for field in salary_dynamic_fields:
                field.field_name = updated_payroll_item.name  # Update the field name with the new value
                field.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Payroll Item updated successfully.",                
                "redirect_url": reverse('payroll:payroll_items')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
                "message": str(message),
                "title": "Form validation error"  
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = PayrollItemForm(instance=instance)
       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Payroll Item :" + instance.da,            
            "redirect": "true",
            "url": reverse('payroll:edit_payrollitem', kwargs={'pk': instance.pk})
        }
        return render(request, 'payroll/payrollitem.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def payroll_item(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(PayrollItem.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Payroll Item'
    }
    return render(request, "payroll_item/payrollitem.html',", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_payroll_item(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(PayrollItem.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    PayrollItem.objects.filter(pk=pk).update(is_deleted=True,da=instance.da + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Payroll Item Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('payroll:payroll_items')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')   


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_salary(request):
    current_company = get_current_company(request)        
    if request.method == 'POST':
        form = SalaryForm(request.POST, current_company=current_company)
        if form.is_valid():
            net_salary = form.cleaned_data['net_salary']
            selected_date = form.cleaned_data['date']
            employee = form.cleaned_data['employee']
            auto_id = get_auto_id(Salary)
            a_id = get_a_id(Salary,request)
            company = current_company
            creator = request.user
            updator = request.user    
            month = selected_date.month
            year = selected_date.year        
            # total_working_days = AttendanceRegister.total_working_days_in_month(year, month)
            if not Salary.objects.filter(date__month=month,date__year=year,employee=employee, company=current_company, is_deleted=False).exists():
                salary=Salary.objects.create(
                    employee=employee,
                    net_salary=net_salary,
                    date = selected_date ,
                    auto_id=auto_id,
                    a_id=a_id,
                    company=company,
                    creator=creator,
                    updator=updator
                )
                payroll_additions_fields = PayrollItem.objects.filter(company=current_company, category='Additions', is_deleted=False)
                payroll_deductions_fields = PayrollItem.objects.filter(company=current_company, category='Deductions', is_deleted=False)

                # Save dynamic fields for additions
                for item in payroll_additions_fields:
                    field_name = item.name
                    # Check if the same field already exists for the current employee's salary
                    if not SalaryDynamicField.objects.filter(company=current_company, employee=employee, salary=salary, field_name=field_name).exists():
    
                        field_value = request.POST.get(field_name, 0)
                        try:
                            field_value = Decimal(field_value)
                        except (InvalidOperation, ValueError):
                            # If conversion fails, log the error and use 0 as a default value
                            print(f"Invalid input for {field_name}: {field_value}. Defaulting to 0.")
                            field_value = Decimal('0.00')

                        # Check if field_value is NaN (Not a Number)
                        if field_value.is_nan():
                            # If so, default it to 0
                            field_value = Decimal('0.00')
            
                        SalaryDynamicField.objects.create(company=current_company,employee=employee, salary=salary, field_name=field_name, field_value=field_value, category='Additions')

                # Save dynamic fields for deductions
                for item in payroll_deductions_fields:
                    field_name = item.name
                    field_value = request.POST.get(field_name, 0)
                    try:
                        # Attempt to convert field_value to Decimal
                        field_value = Decimal(field_value)
                    except (InvalidOperation, ValueError):
                        # If conversion fails, log the error and use 0 as a default value
                        print(f"Invalid input for {field_name}: {field_value}. Defaulting to 0.")
                        field_value = Decimal('0.00')

                    # Check if field_value is NaN (Not a Number)
                    if field_value.is_nan():
                        # If so, default it to 0
                        field_value = Decimal('0.00')
                    SalaryDynamicField.objects.create(company=current_company,employee=employee, salary=salary, field_name=field_name, field_value=field_value, category='Deductions')
       
                net_salary_in_words = num2words(net_salary, lang='en')
                # Convert the entire string to uppercase
                net_salary_in_words = net_salary_in_words.upper()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Salary created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('payroll:salaries')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Salary already exists",                        
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = SalaryForm(current_company=current_company)
        # Retrieve dynamic fields for additions and deductions
        additions_fields = [item.name for item in PayrollItem.objects.filter(company=current_company, category='Additions', is_deleted=False)]
        deductions_fields = [item.name for item in PayrollItem.objects.filter(company=current_company, category='Deductions', is_deleted=False)]
        context = {
            "title": "Create Salary",
            "form": form,
            "additions_fields": additions_fields,
            "deductions_fields": deductions_fields,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'payroll/salary.html', context)
    

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def salaries(request):
    current_company = get_current_company(request)
    salaries = Salary.objects.filter(company=current_company,is_deleted=False)    
    
    employee_name_query = request.GET.get("employee_name")
    if employee_name_query:
        salaries = salaries.filter(Q(employee__firstname__icontains=employee_name_query) | Q(employee__lastname__icontains=employee_name_query))    
    employee_designation_query = request.GET.get("employee_designation")
    if employee_designation_query:
        salaries = salaries.filter(Q(employee__designation__name__icontains=employee_designation_query))    
    month_query = request.GET.get("month")
    if month_query:
        month_int = timezone.datetime.strptime(month_query, "%B").month    # Convert month name to its corresponding number
        salaries = salaries.filter(date__month=month_int)    
    year_query = request.GET.get("year")
    if year_query:
        salaries = salaries.filter(Q(date__year__icontains=year_query))    
    
    paginator = Paginator(salaries,1000000000000)
    page_number = request.GET.get('page')
    salaries = paginator.get_page(page_number)


    # Retrieve dynamic fields for additions and deductions
    additions_fields = PayrollItem.objects.filter(company=current_company, category='Additions', is_deleted=False)
    deductions_fields = PayrollItem.objects.filter(company=current_company, category='Deductions', is_deleted=False)
    employees = Employee.objects.filter(company=current_company, is_deleted=False)

    # Retrieve the current values of additions and deductions
    dynamic_fields = SalaryDynamicField.objects.filter(company=current_company, is_deleted=False)
    additions_values = {item.field_name: item.field_value for item in dynamic_fields if item.category == 'Additions'}
    deductions_values = {item.field_name: item.field_value for item in dynamic_fields if item.category == 'Deductions'}
    
    # Remove duplicates from additions_data
    seen = set()
    unique_additions_data = []
    for field in additions_fields:
        if field.name not in seen:
            unique_additions_data.append({'name': field.name, 'value': additions_values.get(field.name, '')})
            seen.add(field.name)
    
    deductions_data = [{'name': field.name, 'value': deductions_values.get(field.name, '')} for field in deductions_fields]

    context = {
        'salaries': salaries,
        "title": 'Salary List' ,
        "employees":employees,
        "additions_fields": additions_fields,
        "deductions_fields": deductions_fields,
        "additions_data": unique_additions_data,
        "deductions_data": deductions_data

    }
    return render(request, "payroll/salary.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_salary(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Salary.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=instance, current_company=current_company)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Salary updated successfully.",                
                "redirect_url": reverse('payroll:salaries')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
                "message": str(message),
                "title": "Form validation error"  
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = SalaryForm(instance=instance, current_company=current_company) 
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Salary :" + instance.employee,   
            "redirect": "true",
            "url": reverse('payroll:edit_salary', kwargs={'pk': instance.pk})
        }
        return render(request, 'payroll/salary.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_salary(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Salary.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    Salary.objects.filter(pk=pk).update(is_deleted=True)
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Salary Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('payroll:salaries')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def payslip(request,pk): 
    current_company = get_current_company(request)    
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    salaries = Salary.objects.filter(company=current_company,is_deleted=False)
    instance = Salary.objects.get(pk=pk,company=current_company,is_deleted=False)
    employee = instance.employee
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')
    # Convert the entire string to uppercase
    net_salary_in_words = net_salary_in_words.upper()
    context = {
        'pk':pk,
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }
    return render(request, "payroll/payslip.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def print_payslip(request,pk): 
    current_company = get_current_company(request)    
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    salaries = Salary.objects.filter(company=current_company,is_deleted=False)
    instance = Salary.objects.get(pk=pk,company=current_company,is_deleted=False)
    employee = instance.employee
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')
    # Convert the entire string to uppercase
    net_salary_in_words = net_salary_in_words.upper()
    context = {
        'pk':pk,
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }
    return render(request, "payroll/print_payslip.html", context)


def print_employee_payslip(request,pk): 
    salaries = Salary.objects.filter(is_deleted=False)
    instance = Salary.objects.get(pk=pk,is_deleted=False)

    current_company = instance.company  
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    # Access the Employee instance directly from the Salary instance
    employee = instance.employee
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')
    # Convert the entire string to uppercase
    net_salary_in_words = net_salary_in_words.upper()
    context = {
        'pk':pk,
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }
    return render(request, "payroll/print_employee_payslip.html", context)


def generate_payslip_pdf(request, pk=None):
    pk=request.GET.get('pk')
    current_company = get_current_company(request)    
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    if pk is not None:
        instance = get_object_or_404(Salary, pk=pk, company=current_company, is_deleted=False)
    elif 'pk' in request.GET:
        pk = request.GET.get('pk')
        instance = get_object_or_404(Salary, pk=pk, company=current_company, is_deleted=False)
    else:
        # Handle the case when pk is not provided or found in request.GET
        return HttpResponse("No primary key provided.")
    employee = instance.employee
    # Get the month from the date field of the Salary model
    salary_month = instance.date.strftime('%B %Y')
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')   
    template_path = 'payroll/payslip-pdf.html'
    context = {
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }    
    response = HttpResponse(content_type = 'application/pdf')
    # Generate a slugified version of the employee name and concatenate it with the month
    filename = f"payslip_{slugify(employee)}_{salary_month}.pdf"
    response['Content-Disposition'] = f'filename="{filename}"'  
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse("we had some errors <pre>" + html + "</pre>")
    return response


def generate_email_payslip_pdf(request, pk):
    instance = Salary.objects.get(pk=pk,is_deleted=False)
    employee = instance.employee    
    current_company = instance.company 
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    # Get the month from the date field of the Salary model
    salary_month = instance.date.strftime('%B %Y')
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')   
    template_path = 'payroll/payslip-employee-pdf.html'
    context = {
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }    
    response = HttpResponse(content_type = 'application/pdf')
    # Generate a slugified version of the employee name and concatenate it with the month
    filename = f"payslip_{slugify(employee)}_{salary_month}.pdf"
    response['Content-Disposition'] = f'filename="{filename}"'  
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse("we had some errors <pre>" + html + "</pre>")
    return response



def generate_employee_payslip_pdf(request, pk=None):
    pk=request.GET.get('pk')
    instance = Salary.objects.get(pk=pk,is_deleted=False)
    employee = instance.employee    
    current_company = instance.company 
    currency=current_company.country.currency
    currency_symbol = current_company.country.currency_symbol
    # Get the month from the date field of the Salary model
    salary_month = instance.date.strftime('%B %Y')
    dynamic_fields =  SalaryDynamicField.objects.filter(company=current_company,employee=employee,is_deleted=False)
    # Filter SalaryDynamicField objects for the current Salary instance, separated by category
    additions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Additions')
    deductions_fields = SalaryDynamicField.objects.filter(company=current_company,employee=employee, salary=instance, category='Deductions')
     # Calculate total of additions
    total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')    
    # Calculate total of deductions
    total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
    # Convert net_salary to words without specifying currency
    net_salary_in_words = num2words(instance.net_salary, lang='en')   
    template_path = 'payroll/payslip-employee-pdf.html'
    context = {
        'instance': instance,
        'title': 'PaySlip',
        'currency': currency,
        'currency_symbol':currency_symbol,
        'dynamic_fields': dynamic_fields,
        'additions_fields': additions_fields,
        'deductions_fields': deductions_fields,
        'total_additions': total_additions,
        'total_deductions': total_deductions,
        'net_salary_in_words': net_salary_in_words
    }    
    response = HttpResponse(content_type = 'application/pdf')
    # Generate a slugified version of the employee name and concatenate it with the month
    filename = f"payslip_{slugify(employee)}_{salary_month}.pdf"
    response['Content-Disposition'] = f'filename="{filename}"'  
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse("we had some errors <pre>" + html + "</pre>")
    return response



@login_required
@user_passes_test(has_employee_dashboard_permission, redirect_field_name=None)
def payslips_employee(request):
    try:
        employee = get_object_or_404(Employee, user=request.user, is_deleted=False)
        company=employee.company
        payslips = Salary.objects.filter(company=company,employee=employee,is_deleted=False)
        # Filter SalaryDynamicField objects for the current Salary instance, separated by category
        additions_fields = SalaryDynamicField.objects.filter(company=company,employee=employee, category='Additions')
        deductions_fields = SalaryDynamicField.objects.filter(company=company,employee=employee, category='Deductions')
        # Calculate total of additions
        total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')        
        # Calculate total of deductions
        total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
        context = {
            'company':company,
            'employee': employee,
            'payslips': payslips,
            'title': 'PaySlip',
            'additions_fields': additions_fields,
            'deductions_fields': deductions_fields,
            'total_additions': total_additions,
            'total_deductions': total_deductions
        }
        return render(request, "payroll/payslips-employee.html", context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found for the user.")
    
    
@login_required
@user_passes_test(has_employee_dashboard_permission, redirect_field_name=None)
def employee_payslip(request,pk):
    try:
        employee = get_object_or_404(Employee, user=request.user, is_deleted=False)
        company=employee.company
        currency=company.country.currency
        currency_symbol = company.country.currency_symbol
        instance = Salary.objects.get(pk=pk,employee=employee,company=company,is_deleted=False)
        # Filter SalaryDynamicField objects for the current Salary instance, separated by category
        additions_fields = SalaryDynamicField.objects.filter(company=company,employee=employee, salary=instance, category='Additions')
        deductions_fields = SalaryDynamicField.objects.filter(company=company,employee=employee, salary=instance, category='Deductions')
        # Calculate total of additions
        total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')        
        # Calculate total of deductions
        total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
        # Convert net_salary to words without specifying currency
        net_salary_in_words = num2words(instance.net_salary, lang='en')
        # Convert the entire string to uppercase
        net_salary_in_words = net_salary_in_words.upper()
        context = {
            'pk':pk,
            'instance': instance,
            'title': 'PaySlip',
            'currency': currency,
            'currency_symbol':currency_symbol,
            'additions_fields': additions_fields,
            'deductions_fields': deductions_fields,
            'total_additions': total_additions,
            'total_deductions': total_deductions,
            'net_salary_in_words': net_salary_in_words
        }
        return render(request, "payroll/payslip-employee.html", context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found for the user.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")


def email_payslip(request, pk=None):
    pk = request.GET.get('pk')
    try:
        current_company = get_current_company(request)
        currency = current_company.country.currency
        currency_symbol = current_company.country.currency_symbol
        salary = get_object_or_404(Salary, pk=pk, company=current_company, is_deleted=False)
        employee = salary.employee
        month = salary.date.strftime("%B %Y")
        net_salary = salary.net_salary
        additions_fields = SalaryDynamicField.objects.filter(
            company=current_company,
            employee=employee,
            salary=salary,
            category='Additions'
        )
        deductions_fields = SalaryDynamicField.objects.filter(
            company=current_company,
            employee=employee,
            salary=salary,
            category='Deductions'
        )

        # Calculate total of additions and deductions
        total_additions = additions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
        total_deductions = deductions_fields.aggregate(Sum('field_value'))['field_value__sum'] or Decimal('0.00')
        net_salary_in_words = num2words(net_salary, lang='en').upper()

        # Generate payslip PDF
        payslip_pdf_response = generate_email_payslip_pdf(request, pk=salary.id)
        if not isinstance(payslip_pdf_response, HttpResponse):
            return HttpResponseServerError("Error generating payslip PDF")

        payslip_pdf_content = payslip_pdf_response.content
        payslip_pdf_bytes = BytesIO(payslip_pdf_content)

        employee_name_with_underscores = employee.get_full_name.replace(' ', '_')
        payslip_filename = f"payslip_{employee_name_with_underscores}_{month}.pdf"

        subject = f'PaySlip for the month - {month}'
        context = {
            'pk': salary.id,
            'instance': salary,
            'title': 'PaySlip',
            'currency': currency,
            'currency_symbol': currency_symbol,
            'additions_fields': additions_fields,
            'deductions_fields': deductions_fields,
            'total_additions': total_additions,
            'total_deductions': total_deductions,
            'net_salary_in_words': net_salary_in_words
        }
        html_message = render_to_string('payroll/payslip-employee-pdf.html', context=context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = employee.email

        # Call the Celery task
        send_mail_payslip.delay(subject, plain_message, html_message, from_email, to_email, payslip_filename, payslip_pdf_bytes.getvalue())

        response_data = {
            "status": "true",
            "title": "Email sent Successfully",
            "message": "Payslip Sent in email successfully.",
            "redirect": "true"
        }
    except Salary.DoesNotExist:
        response_data = {
            "status": "false",
            "stable": "true",
            "title": "Not Found",
            "message": "Salary not found",                        
        }
    except Exception as e:
        response_data = {
            "status": "false",
            "stable": "true",
            "title": "Error sending in email",
            "message": f"Error sending in email: {e}",                        
        }
    return JsonResponse(response_data)
