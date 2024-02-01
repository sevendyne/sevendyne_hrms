import datetime
import json
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from employee import models
from employee.forms import DepartmentForm, DesignationForm, EmployeeForm, LeaveTypeForm
from employee.models import Department, Designation, Employee, Leave, LeaveType
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
        departments = Department.objects.all()
        print("edit get request - designation")
        print("instance",instance)
        print("departmet",instance.department)
        print("designation",instance.name)
        context = {
            "form": form,
            "instance": instance,
            "departments":departments,
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
@company_required
def create_leave(request):
    current_company = get_current_company(request)
    print("current comapny",current_company)
    if request.method == 'POST':
        print("leave type post request")
        form = LeaveForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            days = form.cleaned_data['days']
            auto_id = get_auto_id(Leave)
            a_id = get_a_id(Leave,request)
            company = current_company
            creator = request.user
            updator = request.user

            if not Leave.objects.filter(name=name,company=current_company,is_deleted=False).exists():
                Leave(                    
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
                    "message": "Leave created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('employee:leaves')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Leave already exists",                        
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


@login_required
@company_required
def leaves(request):
    current_company = get_current_company(request)
    leaves = Leave.objects.filter(company=current_company,is_deleted=False)
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
def edit_leave(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Leave.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("department id",instance.pk)
    if request.method == "POST":
        form = LeaveForm(request.POST, instance=instance)

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
                "message": "Leave updated successfully.",                
                "redirect_url": reverse('employee:leaves')
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
            "title": "Edit Leave :" + instance.name,
            
            "redirect": "true",
            "url": reverse('employee:edit_leave', kwargs={'pk': instance.pk}),
        }
        return render(request, 'leave/leaves.html', context)


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
def delete_leave(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Leave.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Leave.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Leave Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('employee:leaves')
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


