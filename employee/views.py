import datetime
import json
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from employee.forms import DepartmentForm, DesignationForm
from employee.models import Department, Designation
from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company
from django.urls import reverse


# Company crud starts here
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
                    user.groups.add(employee)
                    hashed_password = make_password(password)
                    user.save()
                hashed_password = make_password(password)
                user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'firstname': firstname, 'lastname': lastname})
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
    employee = Employee.objects.filter(is_deleted=False,is_blocked=False,company=current_company,)
    paginator = Paginator(employee,1000000000000)
    page_number = request.GET.get('page')
    employee = paginator.get_page(page_number)
    context = {
        'employee': employee,
        "title": 'Employee' 
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
   
