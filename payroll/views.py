import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from employee.models import Employee

from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company
from payroll.forms import PayrollItemForm, SalaryForm, SalarySettingForm
from payroll.models import  PayrollItem, Salary, SalaryData, SalarySetting

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
                "redirect_url": reverse('payroll:salaries_settings')
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
        "redirect_url" : reverse('payroll:salaries_settings')
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

# @login_required
# @company_required
# def create_salary(request):
#     current_company = get_current_company(request)    
#     if request.method == 'POST':
#         form = SalaryForm(request.POST)
#         if form.is_valid():
#             # payroll_item = form.cleaned_data['payroll_item']
#             net_salary = form.cleaned_data['net_salary']
#             employee = form.cleaned_data['employee']
#             auto_id = get_auto_id(Salary)
#             a_id = get_a_id(Salary,request)
#             company =current_company
#             creator = request.user
#             updator = request.user

#             if not Salary.objects.filter(employee=employee,company=current_company,is_deleted=False).exists():
#                 salary_instance = Salary.objects.create(
#                     employee=employee,
#                     net_salary=net_salary,
#                     auto_id=auto_id,
#                     a_id=a_id,
#                     company=company,
#                     creator=creator,
#                     updator=updator
#                 )
#                 # payroll_items = {}
#                 # for key, value in request.POST.items():
#                 #     if key != 'csrfmiddlewaretoken' and key != 'employee' and key != 'net_salary':
#                 #         payroll_items[key] = value
#                 #         print(f"{key} ------ {value}")

#                 # # Print all payroll items data in the terminal
#                 # print("All payroll items data:")
#                 # for item_name, item_value in payroll_items.items():
#                 #     print(f"{item_name}: {item_value}")

#                 # Extract payroll items
#                 payroll_items = {'Additions': {}, 'Deductions': {}}
#                 for key, value in request.POST.items():
#                     if key != 'csrfmiddlewaretoken' and key != 'employee' and key != 'net_salary':
#                         payroll_item_name = key
#                         if value:
#                             payroll_item_value = value
#                         else:
#                             payroll_item_value = 0
#                         print("payroll item name ",payroll_item_name)
#                         print("payroll item value ",payroll_item_value)
#                         # Get the category of the payroll item
#                         # try:
#                         #     payroll_item = PayrollItem.objects.filter(name=payroll_item_name, company=current_company, is_deleted=False)
#                         #     if payroll_item:
#                         #         category = payroll_item.category
#                         #         payroll_items[category][payroll_item_name] = payroll_item_value  
#                         #         print("payroll_item_name",payroll_item_name)
#                                 # Save basic salary separately in Payslip model
#                         if payroll_item_name == 'Basic Salary':
#                             print("payroll item is basic salary")
#                             # Retrieve the PayrollItem instance for basic salary
#                             try:
#                                 basic_salary_item = PayrollItem.objects.get(name='Basic Salary', category='Additions', company=current_company, is_deleted=False)
#                                 print("basic_salary_item",basic_salary_item)
#                                 # Create a Payslip instance for basic salary
#                                 PaySlip.objects.create(
#                                     company=company,
#                                     employee=employee,
#                                     salary=salary_instance,
#                                     payroll_item=basic_salary_item,
#                                     value=payroll_item_value,
#                                     category='Additions'  # Assuming basic salary is always an addition
#                                 )
#                             except PayrollItem.DoesNotExist:
#                                 print("payroll item with basic salary not exist")
#                                 pass

#                         else:       
#                             print("payroll item is not basic salary")
#                             # if payroll_item_name == 'Basic Salary':
#                             #     print("basic salary comes in else part also")
#                             # PaySlip.objects.bulk_create([
#                             #     PaySlip(salary=salary_instance, payroll_item=payroll_item, value=value, category=category)
#                             #     for payroll_item, value in payroll_items[category].items()
                
#                 # Create PaySlip instances for other payroll items
#                 for category, items in payroll_items.items():
#                     print(f"\nCategory: {category}")
#                     for item_name, item_value in items.items():
#                         print(f"{item_name}: {item_value}")
#                         payroll_item = PayrollItem.objects.get(name=item_name, company=current_company, is_deleted=False)
#                         PaySlip.objects.bulk_create([
#                             PaySlip(salary=salary_instance, payroll_item=payroll_item, value=item_value, category=category)
#                         ])

#                 # Now 'payroll_items' dictionary contains the payroll items data grouped by category
#                 payslips = PaySlip.objects.all()
#                 print("payslips",payslips)
#                 # Print all payroll items data in the terminal
#                 print("All payroll items data:")
#                 for category, items in payroll_items.items():
#                     print(f"\nCategory: {category}")
#                     for item_name, item_value in items.items():
#                         print(f"{item_name}: {item_value}")


#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Salary created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('payroll:salaries')
#                 }
            
#             else:               
#                 response_data = {
#                     "status": "false",
#                     "stable": "true",
#                     "title": "Already exists",
#                     "message": "Salary already exists",                        
#                 }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "form_error",
#                 "title": "Form validation error",
#                 "message": str(message),               
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = SalaryForm()
#         addition_payroll_items = PayrollItem.objects.filter(company=current_company,category='Additions')
#         deduction_payroll_items = PayrollItem.objects.filter(company=current_company,category='Deductions')
        
#         context = {
#             "title": "Create Salary",
#             "form": form,
#             'addition_payroll_items': addition_payroll_items,
#             'deduction_payroll_items': deduction_payroll_items,
#             "redirect": "true",
#             "create":True
#         }
        
#         return render(request, 'payroll/salary.html', context)

# @login_required
# @company_required
# def create_salary(request):
#     current_company = get_current_company(request)
#     if request.method == 'POST':
#         form = SalaryForm(request.POST)
#         if form.is_valid():
#             net_salary = form.cleaned_data['net_salary']
#             employee = form.cleaned_data['employee']
#             auto_id = get_auto_id(Salary)
#             a_id = get_a_id(Salary,request)
#             company = current_company
#             creator = request.user
#             updator = request.user

#             if not Salary.objects.filter(employee=employee, company=current_company, is_deleted=False).exists():
#                 # salary_instance = Salary.objects.create(
#                 #     employee=employee,
#                 #     net_salary=net_salary,
#                 #     auto_id=auto_id,
#                 #     a_id=a_id,
#                 #     company=company,
#                 #     creator=creator,
#                 #     updator=updator
#                 # )

            
#                 payroll_items = {'Additions': [], 'Deductions': []}
#                 for key, value in request.POST.items():
#                     if key != 'csrfmiddlewaretoken' and key != 'employee' and key != 'net_salary':
#                         payroll_item_name = key
#                         if value:
#                             payroll_item_value = value
#                         else:
#                             payroll_item_value = 0

#                         # Fetch the payroll items matching the name, company, and not deleted
#                         payroll_items_queryset = PayrollItem.objects.filter(name=payroll_item_name, company=current_company, is_deleted=False)

#                         # Iterate over each payroll item in the queryset
#                         for payroll_item in payroll_items_queryset:
#                             # Determine category and append to corresponding list
#                             category = payroll_item.category
#                             payroll_items[category].append({'item': payroll_item, 'value': payroll_item_value})

               

#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Salary created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('payroll:salaries')
#                 }
            
#             else:               
#                 response_data = {
#                     "status": "false",
#                     "stable": "true",
#                     "title": "Already exists",
#                     "message": "Salary already exists",                        
#                 }
#         else:
#             message = generate_form_errors(form, formset=False)
#             response_data = {
#                 "stable": "true",
#                 "status": "form_error",
#                 "title": "Form validation error",
#                 "message": str(message),               
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/json')
#     else:
#         form = SalaryForm()
#         addition_payroll_items = PayrollItem.objects.filter(company=current_company, category='Additions')
#         deduction_payroll_items = PayrollItem.objects.filter(company=current_company, category='Deductions')
        
#         context = {
#             "title": "Create Salary",
#             "form": form,
#             'addition_payroll_items': addition_payroll_items,
#             'deduction_payroll_items': deduction_payroll_items,
#             "redirect": "true",
#             "create":True
#         }
        
#         return render(request, 'payroll/salary.html', context)

@login_required
@company_required
def create_salary(request):
    current_company = get_current_company(request)
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            net_salary = form.cleaned_data['net_salary']
            employee = form.cleaned_data['employee']
            # basic_salary = request.POST.get('Basic Salary')
            auto_id = get_auto_id(Salary)
            a_id = get_a_id(Salary,request)
            company = current_company
            creator = request.user
            updator = request.user

            # Retrieve values of addition and deduction payroll items
            # additions = []
            # deductions = []
            # for key, value in request.POST.items():
            #     if key.startswith('addition_'):
            #         additions.append((key.split('_')[1], value))
            #     elif key.startswith('deduction_'):
            #         deductions.append((key.split('_')[1], value))


            # Ensure the employee is valid
            # employee_instance = get_object_or_404(Employee, pk=employee.pk, is_deleted=False)


            if not Salary.objects.filter(employee=employee, company=current_company, is_deleted=False).exists():
                # Create the Salary instance
                Salary.objects.create(
                    employee=employee,
                    net_salary=net_salary,
                    auto_id=auto_id,
                    a_id=a_id,
                    company=company,
                    creator=creator,
                    updator=updator
                )
                
                # # Fetch all relevant payroll items in one database query
                # payroll_items = PayrollItem.objects.filter(name__in=request.POST.keys(), company=current_company, is_deleted=False)

                # # Process payroll items from the form data
                # for payroll_item in payroll_items:
                #     payroll_item_value = request.POST.get(payroll_item.name, 0)
                #     if payroll_item_value:
                #         # Create PaySlip instance for each matching payroll item
                #         category = payroll_item.category
                #         PaySlip.objects.create(
                #             salary=salary_instance,
                #             payroll_items=payroll_item,
                #             # value=payroll_item_value,
                #             # category=category
                #         )
                #         # Add the payroll item to the many-to-many field
                #         payslip.payroll_items.add(payroll_item)
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
        form = SalaryForm()
        addition_payroll_items = PayrollItem.objects.filter(company=current_company, category='Additions')
        deduction_payroll_items = PayrollItem.objects.filter(company=current_company, category='Deductions')
        
        context = {
            "title": "Create Salary",
            "form": form,
            'addition_payroll_items': addition_payroll_items,
            'deduction_payroll_items': deduction_payroll_items,
            "redirect": "true",
            "create":True
        }
        
        return render(request, 'payroll/salary.html', context)

def process_salary_data(request):
    print("process salary data request in views")
    current_company = get_current_company(request)
    # print("current company", current_company)
    # print("current_company.id ",current_company.id )
    form_data = request.POST.dict() 

    print("form data/post dict is ", form_data)
    # Access data from the request.POST dictionary
    # form_data = request.POST.get('formData')  # Get formData
    employee_id = request.POST.get('employee')  # Get employee
    # net_salary = request.POST.get('net_salary')  # Get net_salary
    
    # print("form_data",form_data)
    # print("employee id",employee_id)
    # print("net_salary",net_salary)

    # employee_id = form_data.pop('employee')  # Remove employee from form_data and get its value
    # net_salary = form_data.pop('net_salary')  # Remove net_salary from form_data and get its value

    
    # Retrieve the Employee instance corresponding to the employee_id
    employee = Employee.objects.get(id=employee_id)
    # print("employee",employee)
    salarydata = SalaryData.objects.filter(company=current_company,employee=employee,is_deleted=False)
    print("salarydata",salarydata)
    # if  not SalaryData.objects.filter(company=current_company,employee=employee,is_deleted=False).exists():

    # Create an instance of SalaryData with dynamically created fields
    salary_data_instance = SalaryData.create_dynamic_fields(current_company,form_data)
    print("salary_data_instance after creating dynamic field",salary_data_instance)

     # Print all the dynamically created fields
    # dynamic_fields = salary_data_instance.get_dynamic_fields()
    # print("dynamic fields",dynamic_fields)
    # for field in dynamic_fields:
    #     print(f"{field.verbose_name}: {getattr(salary_data_instance, field.name)}")


    # Set the employee attribute of the instance
    # salary_data_instance.employee = employee
    # print("salary_data_instance.employee",salary_data_instance.employee)
    # salary_data_instance.salary = salary
    # Set the net_salary attribute of the instance
    # salary_data_instance.net_salary = net_salary
    # print("salary_data_instance.net_salary",salary_data_instance.net_salary)
    
    # Set the company attribute of the instance
    # salary_data_instance.company = current_company
    # print("salary_data_instance.company",salary_data_instance.company)  
    # Save the instance to the database
    salary_data_instance.save()
    print("salary_data_instance",salary_data_instance)
        
    return JsonResponse({'success': True})
# except Exception as e:
#     return JsonResponse({'success': False, 'error': str(e)})
    # else:
    #     print("Salary already exists for this employee")
    #     return JsonResponse({'success': False, 'error': 'Salary already exists for this employee'})
@login_required
@company_required
def payslip(request,pk):
    print("payslip request in views got")
    current_company = get_current_company(request)
    salary_data = get_object_or_404(SalaryData.objects.filter(company=current_company,is_deleted=False,employee__id=pk))
    print("salary datas",salary_data)

    # Iterate through each SalaryData instance
    # for salary_data in salary_datas:
        # Print the fields and their values for the current instance
    # Print the dynamic fields and their values for the salary_data instance
    dynamic_fields = {}  # Dictionary to store dynamic field values
    print("salary_data.get_dynamic_fields()",salary_data.get_dynamic_fields())
    # Iterate through each dynamic field of the salary_data instance
    for field in salary_data.get_dynamic_fields():
        # Use getattr to access the value of each dynamic field
        field_value = getattr(salary_data, field.name)
        # Add the field name and value to the dynamic_fields dictionary
        dynamic_fields[field.name] = field_value

        # Add a separator for better readability between instances
        print("=" * 20)
    instance = get_object_or_404(SalaryData.objects.filter(employee__pk=pk,company=current_company,is_deleted=False))

    context = {
        'salary_data':salary_data,
        'dynamic_fields': dynamic_fields, 
        'instance': instance,
        'title': 'Pay Slip',

    }
    return render(request, "payroll/payslip.html", context)


# @login_required
# @company_required
# def payslip(request, pk):
    
#     current_company = get_current_company(request)

#     salary_instance = get_object_or_404(Salary.objects.filter(pk=pk, company=current_company, is_deleted=False))
#     # employee_instance = salary_instance.employee  # Retrieve the employee associated with the salary
    
#     instance = get_object_or_404(PaySlip.objects.filter(salary=salary_instance, is_deleted=False))

#     context = {
#         'instance': instance,
#         'title': 'Pay Slip',
#     }
#     return render(request, "payroll/payslip.html", context)


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
    
    Salary.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Salary Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('payroll:salaries')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   