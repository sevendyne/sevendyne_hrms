import calendar
import datetime
import json
from django.forms import formset_factory
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from employee import models
from employee.forms import AttendanceDateForm, AttendanceRegisterForm, DepartmentForm, DesignationForm, EmployeeForm, LeaveForm, LeaveTypeForm
from employee.models import AttendanceRegister, Department, Designation, Employee, Leave, LeaveType
from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company
from django.urls import reverse


# Department crud starts here
@login_required
@company_required
def create_department(request):
    current_company = get_current_company(request)
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            auto_id = get_auto_id(Department)
            a_id = get_a_id(Department,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Department.objects.filter(name=name,company=current_company,is_deleted=False).exists():
                Department(                    
                    name = name,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Department created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:departments')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Department already exists",                        
                }
                print("status inside", response_data["status"])
            print("status outside", response_data["status"])
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = DepartmentForm()

        context = {
            "title": "Create Department",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'department/departments.html', context)


@login_required
@company_required
def departments(request):
    current_company = get_current_company(request)
    departments = Department.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(departments,1000000000000)
    page_number = request.GET.get('page')
    departments = paginator.get_page(page_number)
    context = {
        'departments': departments,
        "title": 'Departments' 
    }
    return render(request, "department/departments.html", context)


@login_required
@company_required
def edit_department(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Department.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("department id",instance.pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            print("updated department",data.name)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Department updated successfully.",                
                "redirect_url": reverse('employee:departments')
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
        form = DepartmentForm(instance=instance)

        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Department :" + instance.name,
            
            "redirect": "true",
            "url": reverse('employee:edit_department', kwargs={'pk': instance.pk}),
        }
        return render(request, 'department/departments.html', context)


@login_required
@company_required
def department(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Department.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Department',

    }
    return render(request, "department/department.html", context)

@login_required
@company_required
def delete_department(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Department.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Department.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Department Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:departments')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   


# Designation crud starts here
# @login_required
# @company_required
# def create_designation(request):
#     Designationformset = formset_factory(DesignationFormset)
#     if request.method == 'POST':
#         designation_formset = Designationformset(request.POST, prefix='designation_formset')
#         form =DesignationForm(request.POST)
#         if designation_formset.is_valid() and form.is_valid():
#             department = form.cleaned_data['department']

#             for form in designation_formset:
#                 name = form.cleaned_data['name']                               
#                 auto_id = get_auto_id(Designation)
#                 creator = request.user
#                 updator = request.user
               
#                 if Designation.objects.filter(name=name,is_deleted=False).exists():
#                     is_ok =False
#                 else:
#                     Designation(
#                         department=department,
#                         name = name,
#                         auto_id = auto_id,
#                         creator = creator,
#                         updator = updator
#                     ).save() 
#                     is_ok=True               
#             if is_ok ==True:
#                 response_data = {
#                     "status": "true",
#                     "title": "Successfully Created",
#                     "message": "Designation created successfully.",
#                     "redirect": "true",
#                     "redirect_url": reverse('employee:designations')
#                 }
#             elif is_ok ==False:
#                 response_data = {
#                     "stable": "true",
#                     "title": "Already exists",
#                     "warning" : True
#                 }
#             else :
#                 response_data = {
#                     "stable": "true",
#                     "title": "Formset Error",
#                     "warning" : True
#                 }
#             return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#         else:
#             message = generate_form_errors(designation_formset, formset=True)
#             response_data = {
#                 "stable": "true",
#                 "status": "false",
#                 "message": str(message),
#                 "title": "Form validation error"                
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/javascript')
#     else:
#         designation_formset = Designationformset(prefix='designation_formset')
#         form = DesignationForm()
#         context = {
#             "title": "Create Designation",
#             "designation_formset": designation_formset,
#             'form':form,
#             "redirect": "true",
#             "create":True
#         }
#         return render(request, 'designations/designations.html', context)

@login_required
@company_required
def create_designation(request):
    current_company = get_current_company(request)
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']
            auto_id = get_auto_id(Designation)
            a_id = get_a_id(Designation,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Designation.objects.filter(name=name,department=department,company=current_company,is_deleted=False).exists():
                Designation(                    
                    name = name,
                    department = department,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Designation created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:designations')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Designation already exists",                        
                }
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = DesignationForm()
        print("form get request")
        context = {
            "title": "Create Designation",
            "form": form,
            "redirect": "true",
            "create":True
        }
        
        return render(request, 'designation/designations.html', context)


@login_required
@company_required
def designations(request):
    current_company = get_current_company(request)
    designations = Designation.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(designations,1000000000000)
    page_number = request.GET.get('page')
    designations = paginator.get_page(page_number)
    context = {
        'designations': designations,
        "title": 'Designation' 
    }
    return render(request, "designation/designations.html", context)


@login_required
@company_required
def edit_designation(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Designation.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("edit request, designation name",instance.name)
    if request.method == "POST":
        print("post request")
        form = DesignationForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            print("updated Designation",data.name)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Designation updated successfully.",                
                "redirect_url": reverse('employee:designations')
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
        form = DesignationForm(instance=instance)
        departments = Department.objects.filter(company=current_company,is_deleted=False)
        print("edit get request - designation")
        print("instance",instance)
        print("departmet",instance.department)
        print("designation",instance.name)
        context = {
            "form": form,
            "instance": instance,
            "departments":departments,
            'pk': pk,
            "title": "Edit Designation :" + instance.name,
            
            "redirect": "true",
            "url": reverse('employee:edit_designation', kwargs={'pk': instance.pk}),

        }
        return render(request, 'designation/designations.html', context)


@login_required
@company_required
def designation(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Designation.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Designations',

    }
    return render(request, "designation/designations.html", context)

@login_required
@company_required
def delete_designation(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Designation.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Designation.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Designation Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:designations')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

# Employee Profile crud starts here
@login_required
@company_required
def create_employee(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            client_company = form.cleaned_data['client_company']
            employeeid = form.cleaned_data['employeeid']
            department = form.cleaned_data['department']
            designation = form.cleaned_data['designation']
            auto_id = get_auto_id(Employee)
            a_id = get_a_id(Employee,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Employee.objects.filter(username=username,company=current_company,is_deleted=False).exists():
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    user.groups.add(employee_group)
                    hashed_password = make_password(password)
                    user.save()
                hashed_password = make_password(password)
                user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'first_name': firstname, 'last_name': lastname})

                if created:
                    # Get or create the 'hrms_clients' group
                    employee_group, created = Group.objects.get_or_create(name='employee_group')

                    # Add the user to the 'hrms_clients' group
                    user.groups.add(employee_group)

                    # Save the user to update group membership
                    user.save()

                Employee( 
                    user = user,
                    firstname = firstname,
                    lastname = lastname,
                    email = email,
                    username = username,
                    password = password,
                    phone = phone,
                    address = address,
                    client_company = client_company,
                    department = department,
                    designation = designation,
                    employeeid = employeeid,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Employee created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:employees')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Employee already exists",                        
                }
                print("status inside", response_data["status"])
            print("status outside", response_data["status"])
        else:
            print('not valid form validation error')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
            print("error message",response_data["message"])
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = EmployeeForm()

        context = {
            "title": "Create Employee",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'employee/employees.html', context)


@login_required
@company_required
def employees(request):
    current_company = get_current_company(request)
    employees = Employee.objects.filter(is_deleted=False,is_blocked=False,company=current_company,)
    paginator = Paginator(employees,1000000000000)
    page_number = request.GET.get('page')
    employee = paginator.get_page(page_number)
    context = {
        'employees': employees,
        "title": 'Employees' 
    }
    return render(request, "employee/employees.html", context)


@login_required
@company_required
def edit_employee(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Employee.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("Employee id",instance.pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)

            # Update associated User instance
            user = instance.user
            user.username = data.username
            user.email = data.email
            user.password = make_password(data.password)  # Hash the new password
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.email = data.email
            user.save()

            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            # print("updated Client",data.company)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Employee updated successfully.",                
                "redirect_url": reverse('employee:employees')
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
        form = EmployeeForm(instance=instance)

        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Employee :" + instance.firstname,
            
            "redirect": "true",
            "url": reverse('employee:employeemployee', kwargs={'pk': instance.pk}),


        }
        return render(request, 'employee/employees.html', context)


@login_required
@company_required
def employee(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Employee.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Employee',

    }
    return render(request, 'employee/employees.html', context)

@login_required
@company_required
def delete_employee(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Employee.objects.filter(pk=pk,is_deleted=False))
    
    Employee.objects.filter(pk=pk).update(is_deleted=True,company=current_company,company_name=instance.company_name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Employee Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:employees')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   
# Leave Type crud starts here
@login_required
@company_required
def create_leave_type(request):
    current_company = get_current_company(request)
    print("current comapny",current_company)
    if request.method == 'POST':
        print("leave type post request")
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            days = form.cleaned_data['days']
            auto_id = get_auto_id(LeaveType)
            a_id = get_a_id(LeaveType,request)
            company = current_company
            creator = request.user
            updator = request.user

            if not LeaveType.objects.filter(name=name,company=current_company,is_deleted=False).exists():
                LeaveType(                    
                    name = name,
                    days = days,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Leave Type created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:leave_types')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Leave Type already exists",                        
                }
                print("status inside", response_data["status"])
            print("status outside", response_data["status"])
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = LeaveTypeForm()

        context = {
            "title": "Create Leave Type",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'settings/leave-type.html', context)


@login_required
@company_required
def leave_types(request):
    current_company = get_current_company(request)
    leave_types = LeaveType.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(leave_types,1000000000000)
    page_number = request.GET.get('page')
    leave_types = paginator.get_page(page_number)
    context = {
        'leave_types': leave_types,
        "title": 'Leave Types' 
    }
    return render(request, "settings/leave-type.html", context)


@login_required
@company_required
def edit_leave_type(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(LeaveType.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("department id",instance.pk)
    if request.method == "POST":
        form = LeaveTypeForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            print("updated department",data.name)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Leave Type updated successfully.",                
                "redirect_url": reverse('employee:leave_types')
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
        form = LeaveTypeForm(instance=instance)

        context = {
            "form": form,
            "instance": instance,
            "title": "Edit LeaveType :" + instance.name,
            
            "redirect": "true",
            "url": reverse('employee:edit_leave_type', kwargs={'pk': instance.pk}),
        }
        return render(request, 'settings/leave-type.html', context)


@login_required
@company_required
def leave_type(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(LeaveType.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Leave Type',

    }
    return render(request, "leave/leave.html", context)

@login_required
@company_required
def delete_leave_type(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(LeaveType.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    LeaveType.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Leave Type Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:leave_types')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

# Leave crud starts here
@login_required
def create_leave(request):
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    if request.method == 'POST':
        print("leave type post request")
        form = LeaveForm(request.POST)
        if form.is_valid():
            startdate = form.cleaned_data['startdate']
            enddate = form.cleaned_data['enddate']
            leavetype = form.cleaned_data['leavetype']
            reason = form.cleaned_data['reason']
            leave_days = form.cleaned_data['leave_days']
            remaining_days = form.cleaned_data['remaining_days']
            auto_id = get_auto_id(Leave)
            a_id = get_a_id(Leave,request)
            company = company
            creator = request.user
            updator = request.user
            print("leave type", leavetype)
            print("leave_days",leave_days)
            if int(leave_days)<=int(remaining_days):
                print("next step is saving in leave model db")
                Leave( 
                    startdate = startdate,
                    enddate = enddate,                   
                    leavetype = leavetype,
                    reason = reason,
                    leave_days = leave_days,
                    auto_id = auto_id,
                    a_id = a_id,
                    company = company,
                    employee = employee,
                    creator = creator,
                    updator = updator
                ).save()
                leave= Leave.objects.all()
                print("leaves saved in db model",leave)
                response_data = {
                    "status": "true",
                    "title": "Leave Request",
                    "message": "Requested for Leave successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:leaves')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Can't apply for these much leave days",
                    "message": "Leave days is greater than the remaining days",                        
                }
                print("status inside", response_data["status"])
            print("status outside", response_data["status"])
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "form_error",
                "title": "Form validation error",
                "message": str(message),               
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = LeaveForm()
        context = {
            "title": "Create Leave",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'leave/leaves.html', context)
    
def ajax_load_remaining_days(request):
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    print("company",company)
    leavetype = request.GET.get('leavetype')
    print("leave type ",leavetype)
    name = leavetype
    print("leave name", name)
    approved_leave_days_count = Leave.objects.filter(company=company,employee=employee, leavetype__name=name, is_approved=True).count()
    print("approved_leave_days_count",approved_leave_days_count)
    if LeaveType.objects.filter(name=name,company=company,is_deleted=False).exists():
        # leavetypes  = LeaveType.objects.filter(is_deleted=False,name=name,company=company)
        leavetype = get_object_or_404(LeaveType, is_deleted=False,name=name,company=company)
        leavetype_days = leavetype.days
        print("leavetype_days",leavetype_days)
        data = leavetype_days - approved_leave_days_count
        print("data - remaining days",data)
    else:
        print("leave type not found")
        data="Data Not Found"
    context = {
        'data' : data
    }
    return render(request,'employee/ajax_load_remaining_days.html',context)


@login_required
def leaves(request):
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    leaves = Leave.objects.filter(company=company,is_deleted=False)
    print("leaves",leaves)
    paginator = Paginator(leaves,1000000000000)
    page_number = request.GET.get('page')
    leaves = paginator.get_page(page_number)
    context = {
        'leaves': leaves,
        "title": 'Leaves' 
    }
    return render(request, "leave/leaves.html", context)

@login_required
@company_required
def leave_approvals(request):
    current_company = get_current_company(request)
    leaves = Leave.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(leaves,1000000000000)
    page_number = request.GET.get('page')
    leaves = paginator.get_page(page_number)
    context = {
        'leaves': leaves,
        "title": 'Leaves' 
    }
    return render(request, "leave/leaves-approval.html", context)


@login_required
@company_required
def edit_leave(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Leave.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("leave id",instance.pk)
    if request.method == "POST":
        form = LeaveForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            print("updated leave",data.name)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Leave updated successfully.",                
                "redirect_url": reverse('employee:leave_approvals')
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
        form = LeaveForm(instance=instance)

        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Leave",
            
            "redirect": "true",
            "url": reverse('employee:edit_leave', kwargs={'pk': instance.pk}),
        }
        return render(request, 'leave/leaves-approval.html', context)


@login_required
@company_required
def leave(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Leave.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Leave',

    }
    return render(request, "leave/leaves.html", context)

@login_required
@company_required
def leave_approval(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Leave.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Leave.objects.filter(pk=pk).update(is_approved=True,status='Approved',employee=instance.employee)

    response_data = {
        "status" : "true",        
        "title" : "Successfully Approved",
        "message" : "Leave Request Successfully Approved.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:leave_approvals')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   


# class LeaveManager(models.Manager):
# 	def get_queryset(self):
# 		'''
# 		overrides objects.all() 
# 		return all leaves including pending or approved
# 		'''
# 		return super().get_queryset()



# 	def all_pending_leaves(self):
# 		'''
# 		gets all pending leaves -> Leave.objects.all_pending_leaves()
# 		'''
# 		return super().get_queryset().filter(status = 'pending').order_by('-created')# applying FIFO 




# 	def all_cancel_leaves(self):
# 		return super().get_queryset().filter(status = 'cancelled').order_by('-created')




# 	def all_rejected_leaves(self):
# 		return super().get_queryset().filter(status = 'rejected').order_by('-created')




# 	def all_approved_leaves(self):
# 		'''
# 		gets all approved leaves -> Leave.objects.all_approved_leaves()
# 		'''
# 		return super().get_queryset().filter(status = 'approved')



# 	def current_year_leaves(self):
# 		'''
# 		returns all leaves in current year; Leave.objects.all_leaves_current_year()
# 		or add all_leaves_current_year().count() -> int total 
# 		this include leave approved,pending,rejected,cancelled

# 		'''
# 		return super().get_queryset().filter(startdate__year = datetime.date.today().year)




# ---------------------LEAVE DASHBOARD-------------------------------------------



def leave_creation(request):
	if not request.user.is_authenticated:
		return redirect('accounts:login')
	if request.method == 'POST':
		form = LeaveCreationForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user
			instance.save()


			# print(instance.defaultdays)
			messages.success(request,'Leave Request Sent,wait for Admins response',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:createleave')

		messages.error(request,'failed to Request a Leave,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('dashboard:createleave')


	dataset = dict()
	form = LeaveCreationForm()
	dataset['form'] = form
	dataset['title'] = 'Apply for Leave'
	return render(request,'dashboard/create_leave.html',dataset)
	







def leaves_list(request):
	if not (request.user.is_staff and request.user.is_superuser):
		return redirect('/')
	leaves = Leave.objects.all_pending_leaves()
	return render(request,'dashboard/leaves_recent.html',{'leave_list':leaves,'title':'leaves list - pending'})



def leaves_approved_list(request):
	if not (request.user.is_superuser and request.user.is_staff):
		return redirect('/')
	leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
	return render(request,'dashboard/leaves_approved.html',{'leave_list':leaves,'title':'approved leave list'})



def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/')

	leave = get_object_or_404(Leave, id = id)
	print(leave.user)
	employee = Employee.objects.filter(user = leave.user)[0]
	print(employee)
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})









def approve_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	user = leave.user
	employee = Employee.objects.filter(user = user)[0]
	leave.approve_leave

	messages.error(request,'Leave successfully approved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:userleaveview', id = id)


def cancel_leaves_list(request):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leaves = Leave.objects.all_cancel_leaves()
	return render(request,'dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})



def unapprove_leave(request,id):
	if not (request.user.is_authenticated and request.user.is_superuser):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.unapprove_leave
	return redirect('dashboard:leaveslist') #redirect to unapproved list




def cancel_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.leaves_cancel

	messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

	dataset = dict()
	leave = Leave.objects.all_rejected_leaves()

	dataset['leave_list_rejected'] = leave
	return render(request,'dashboard/rejected_leaves_list.html',dataset)



def reject_leave(request,id):
	dataset = dict()
	leave = get_object_or_404(Leave, id = id)
	leave.reject_leave
	messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:leavesrejected')

	# return HttpResponse(id)


def unreject_leave(request,id):
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

	return redirect('dashboard:leavesrejected')


@login_required
@company_required
def create_attendance_register(request):     
    company=get_current_company(request)   
    AttendanceRegisterFormSet = formset_factory(AttendanceRegisterForm, extra=0)  
    if request.method == 'POST':     
        date_form = AttendanceDateForm(request.POST)               
        attendanceregister_formset = AttendanceRegisterFormSet(request.POST,prefix='attendanceregister_formset')   

        if attendanceregister_formset.is_valid() and date_form.is_valid(): 

            date = date_form.cleaned_data['date']
            an_fn = date_form.cleaned_data['an_fn']
            for f in attendanceregister_formset:
                is_attended = f.cleaned_data['is_attended'] 
                employee_pk = f.cleaned_data['employee_pk'] 
                employee = Employee.objects.get(pk=employee_pk) 
                is_fn = False 
                is_an = False
                if not AttendanceRegister.objects.filter(employee = employee,date = date,company=company).exists():
                    AttendanceRegister(  
                        employee = employee,
                        date = date,
                        company=company,
                        auto_id = get_auto_id(AttendanceRegister),
                        a_id = get_a_id(AttendanceRegister, request),
                        creator = request.user,
                        updator = request.user,  
                    ).save() 
                att = AttendanceRegister.objects.filter(employee = employee,date = date,company=company)[0]  
                
                if an_fn == "FN" :
                    att.is_fn = is_attended
                if an_fn == "AN" :
                    att.is_an = is_attended
                att.save()
            response_data = {
                "status": "true",
                "redirect": "true",
                "title": "Successfully Created",
                "message": "Attendance Registered Successfully.",
                "redirect_url" : reverse('employee:attendance_register')
            }
        else:
            message = generate_form_errors(date_form,formset=False)
      
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form Validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        att = AttendanceRegister.objects.filter(company=company,is_deleted=False).values('is_attended','is_fn','is_an')
        initial_data={
            'date': datetime.datetime.today().date()
        }
        date_form = AttendanceDateForm(initial= initial_data)               
        employees = Employee.objects.filter(is_deleted=False).order_by('id')
        initial_dict = []
        for s in employees:
            init_dict={
                'employee_name':s.get_full_name,           
                'employee_pk' : s.pk, 
            }
            initial_dict.append(init_dict) 
        attendanceregister_formset = AttendanceRegisterFormSet(prefix='attendanceregister_formset',initial=initial_dict)
        
        context = {
            "title": "Take Attendance",
            "attendanceregister_formset": attendanceregister_formset,
            'date_form' : date_form
        }
        return render(request, 'attendance-register/create_attendance_register.html', context=context)



@login_required
@company_required
def attendance_register(request):
    company = get_current_company(request)
    employees = Employee.objects.filter(company=company,is_deleted=False).order_by('id')

    y = datetime.date.today().year   
    month = datetime.date.today().month
    
    leap = 0
    if y% 400 == 0:
        leap = 1
    elif y % 100 == 0:
        leap = 0
    elif y% 4 == 0:
        leap = 1
    ar = [1,3,5,7,8,10,12]
    n = 30  
    if month in ar:
        n = 31
    elif month == 2:
        if leap ==1:
            n = 29
        else:
            n = 28

    att_list =[]
    nn = n + 1 
    for employee in employees:
        for i in range(1,nn):
            att = employee.get_attendance(month,i)
            
            result = {
                'employee' : employee,
                'date' : i,
                'month' : month,
                'attendance' : att
            }
            att_list.append(result)
    context={        
        "title" : "Attendance Register" ,
        'month' : calendar.month_name[month],     
        'att_list' :att_list,
        'n' : range(n),
        'nn' : range(nn),
        "employees" : employees
    }
    return render(request, 'attendance/attendance.html', context=context)
    # return render(request, 'attendance-register/attendance_register.html', context=context)


@login_required
@company_required
def edit_attendance_register(request, pk):
    company=get_current_company(request)   
    # instance = get_object_or_404(AttendanceRegister.objects.filter(pk=pk, is_deleted=False,company=company))
    AttendanceRegisterFormSet = formset_factory(AttendanceRegisterForm, extra=0)       
    is_class = request.GET.get('is_class')
    if is_class:
        is_class = True
    else:
        is_class = False
    if request.method == 'POST':     
        date_form = AttendanceDateForm(request.POST)               
        attendanceregister_formset = AttendanceRegisterFormSet(request.POST,prefix='attendanceregister_formset')   

        if attendanceregister_formset.is_valid() and date_form.is_valid(): 

            date = date_form.cleaned_data['date']
            an_fn = date_form.cleaned_data['an_fn']
            for f in attendanceregister_formset:
                is_attended = f.cleaned_data['is_attended'] 
                employee_pk = f.cleaned_data['employee_pk'] 
                employee = Employee.objects.get(pk=employee_pk) 
                is_fn = False 
                is_an = False
                if not AttendanceRegister.objects.filter(employee = employee,date = date,company=company).exists():
                    AttendanceRegister(  
                        employee = employee,
                        date = date,
                        company=company,
                        auto_id = get_auto_id(AttendanceRegister),
                        a_id = get_a_id(AttendanceRegister, request),
                        creator = request.user,
                        updator = request.user,  
                    ).save() 
                att = AttendanceRegister.objects.filter(employee = employee,date = date,company=company)[0]  
                
                if an_fn == "FN" :
                    att.is_fn = is_attended
                if an_fn == "AN" :
                    att.is_an = is_attended    

                att.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Updated",
                    "message": "Attendance Register Updated successfully.",
                    "redirect": "true",
                    "redirect_url" : reverse('employee:attendance_register', kwargs={'pk': pk})
                }
        else:
            message = generate_form_errors(date_form,formset=False)
      
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form Validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        initial_data={
            'date': datetime.datetime.today().date()
        }
        date_form = AttendanceDateForm(initial= initial_data)               
        employees = Employee.objects.filter(is_deleted=False,company=company).order_by('id')
        initial_dict = []
        for s in employees:
            init_dict={
                'employee_name':s.f_name,           
                'employee_pk' : s.pk, 
            }
            initial_dict.append(init_dict) 
        attendanceregister_formset = AttendanceRegisterFormSet(prefix='attendanceregister_formset',initial=initial_dict)
        
        context = {
            "title": "Edit Attendance Register",
            "attendanceregister_formset": attendanceregister_formset,
            'date_form' : date_form,
            'pk' : pk,
        }
        return render(request, 'attendance-register/create_attendance_register.html', context=context)


@login_required
@company_required
def delete_attendance_register(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(AttendanceRegister.objects.filter(pk=pk,is_deleted=False,company=current_company))
    
    AttendanceRegister.objects.filter(pk=pk,company=current_company).update(is_deleted=True,date=instance.date + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Attendance Register Successfully Deleted.", 

        "redirect" : "true",       
        "redirect_url" : reverse('employee:attendance_register')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

