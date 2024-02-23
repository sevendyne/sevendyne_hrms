import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company
from payroll.forms import PayrollItemForm, SalaryForm, SalarySettingForm
from payroll.models import PayrollItem, Salary, SalarySetting

# def ajax_load_da(request):
#     company=get_current_company(request)
#     # Retrieve all SalarySetting objects for the company
#     salary_settings = SalarySetting.objects.filter(company=company)

#     # Select the first SalarySetting object
#     salary_setting = salary_settings.first()
    
#     basic_salary = request.GET.get('basicsalary')
#     print("basic salary ",basic_salary) # Calculate DA based on the basic salary and DA percentage
#     da_value = float(basic_salary) * (float(salary_setting.da) / 100)
#     data = da_value

#     context = {
#         'data' : data,
#         'salary_setting':salary_setting
#     }
#     return render(request,'payroll/ajax_load_da.html',context)

def ajax_load_salary_components(request):
    basic_salary = float(request.GET.get('basic_salary', 0))
     # Retrieve all SalarySetting objects for the company
    company=get_current_company(request)
    salary_settings = SalarySetting.objects.filter(company=company)

    # Select the first SalarySetting object
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
    
# Create your views here.
@login_required
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
                    "redirect_url": reverse('payroll:salary_settings')
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
            "title": "Edit Salary Setting :" + instance.da,
            
            "redirect": "true",
            "url": reverse('payroll:edit_salarysetting', kwargs={'pk': instance.pk}),

        }
        return render(request, 'payroll/salary-settings.html', context)


@login_required
@company_required
def salary_setting(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(SalarySetting.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Salary Setting',

    }
    return render(request, "payroll/salary-settings.html", context)

@login_required
@company_required
def delete_salary_setting(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(SalarySetting.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    SalarySetting.objects.filter(pk=pk).update(is_deleted=True,da=instance.da + "_deleted_" + str(instance.auto_id))

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
@company_required
def payroll_items(request):
    current_company = get_current_company(request)
    payroll_items = PayrollItem.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(payroll_items,1000000000000)
    page_number = request.GET.get('page')
    payroll_items = paginator.get_page(page_number)
    context = {
        'payroll_items': payroll_items,
        "title": 'Payroll Items' 
    }
    return render(request, "payroll/payroll-items.html", context)


@login_required
@company_required
def edit_payroll_item(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(PayrollItem.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = PayrollItemForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()

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
            "url": reverse('payroll:edit_payrollitem', kwargs={'pk': instance.pk}),

        }
        return render(request, 'payroll/payrollitem.html', context)


@login_required
@company_required
def payroll_item(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(PayrollItem.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Payroll Item',

    }
    return render(request, "payroll_item/payrollitem.html',", context)

@login_required
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
   

#salary crud starts here

@login_required
@company_required
def create_salary(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            payroll_item = form.cleaned_data['payroll_item']
            employee = form.cleaned_data['employee']
            auto_id = get_auto_id(SalaryForm)
            a_id = get_a_id(Salary,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Salary.objects.filter(payroll_item=payroll_item,company=current_company,is_deleted=False).exists():
                Salary(
                    payroll_item = payroll_item,
                    employee = employee,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Salary created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('payroll:salary')
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
        form = SalaryForm()
        addition_payroll_items = PayrollItem.objects.filter(company=current_company,category='Additions')
        deduction_payroll_items = PayrollItem.objects.filter(company=current_company,category='Deductions')
        # addition_payroll_items = PayrollItem.objects.filter(category='Additions').values('name')  # Include all the fields you need
        # print("addition_payroll_items",addition_payroll_items)
        # addition_payroll_items_json = json.dumps(list(addition_payroll_items)) 
        # print("addition_payroll_items_json",addition_payroll_items_json)
        context = {
            "title": "Create Salary",
            "form": form,
            'addition_payroll_items': addition_payroll_items,
            'deduction_payroll_items': deduction_payroll_items,
            "redirect": "true",
            "create":True
        }
        
        return render(request, 'payroll/salary.html', context)

@login_required
@company_required
def salaries(request):
    current_company = get_current_company(request)
    salaries = Salary.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(salaries,1000000000000)
    page_number = request.GET.get('page')
    salaries = paginator.get_page(page_number)
    context = {
        'salaries': salaries,
        "title": 'Salary List' 
    }
    return render(request, "payroll/salary.html", context)


@login_required
@company_required
def edit_salary(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Salary.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=instance)

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
                "redirect_url": reverse('payroll:salary')
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
        form = SalaryForm(instance=instance)
       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Salary :" + instance.da,
            
            "redirect": "true",
            "url": reverse('payroll:edit_salary', kwargs={'pk': instance.pk}),

        }
        return render(request, 'payroll/salary.html', context)


@login_required
@company_required
def salary(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Salary.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Salary',

    }
    return render(request, "payroll/salary.html", context)



@login_required
@company_required
def delete_salary(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Salary.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Salary.objects.filter(pk=pk).update(is_deleted=True,da=instance.da + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Salary Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('payroll:salary')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   