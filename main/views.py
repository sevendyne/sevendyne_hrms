import json
import datetime

from django.urls import reverse
from main.decorators import company_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q

from main.decorators import company_required
from main.functions import generate_form_errors, has_admin_dashboard_permission, has_hrms_permission
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_employee_dashboard_permission
from employee.models import AttendanceRegister, Employee, Holiday, Leave, LeaveType
from main.models import Company, CompanyAccess, EmailSetting, Portfolio
from main.forms import CompanyForm, EmailSettingForm, PortfolioForm
from payroll.models import PayrollItem, SalarySetting
from candidate.models import Candidate
from hrms.models import HrmsClient
from client.models import Client
from job.models import Job




def home_hrms(request):
    return render(request, "home/index.html")


def about(request):
    return render(request, 'job_portal/about.html')


def terms_and_conditions(request):
    return render(request, 'job_portal/terms_and_conditions.html')


def privacy_policy(request):
    return render(request, 'job_portal/privacy_policy.html')


def job_portal(request):
    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    location = request.GET.get('location')
    job_categories = Job.objects.filter(is_deleted=False).values_list('job_category', flat=True).distinct()
    job_locations = Job.objects.filter(is_deleted=False).values_list('job_location', flat=True).distinct()
    filter_conditions = Q(is_deleted=False)
    if keyword:
        filter_conditions &= Q(job_title__icontains=keyword) | Q(description__icontains=keyword)
    if category:
        filter_conditions &= Q(job_category__icontains=category)
    if location:
        filter_conditions &= Q(job_location__icontains=location)
    filtered_jobs = Job.objects.filter(filter_conditions)
    jobs = Job.objects.filter(is_deleted=False)
    full_time_jobs = Job.objects.filter(job_type='Full Time',is_deleted=False)
    part_time_jobs = Job.objects.filter(job_type='Part Time',is_deleted=False)
    internship_jobs = Job.objects.filter(job_type='Internship',is_deleted=False)
    contract_jobs = Job.objects.filter(job_type='Contract',is_deleted=False)
    context = {
        'jobs': jobs,
        'filtered_jobs': filtered_jobs,
        'full_time_jobs': full_time_jobs,
        'part_time_jobs': part_time_jobs,
        'internship_jobs': internship_jobs,
        'job_categories':job_categories,
        'job_locations':job_locations,
        'contract_jobs':contract_jobs
    }
    return render(request,"job_portal/index.html",context=context)


def job_list(request):
    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    location = request.GET.get('location')
    filter_conditions = Q(is_deleted=False)
    if keyword:
        filter_conditions &= Q(job_title__icontains=keyword) | Q(description__icontains=keyword)
    if category:
        filter_conditions &= Q(job_category__icontains=category)
    if location:
        filter_conditions &= Q(job_location__icontains=location)
    filtered_jobs = Job.objects.filter(filter_conditions)
    jobs = Job.objects.filter(is_deleted=False)
    full_time_jobs = Job.objects.filter(job_type='Full Time',is_deleted=False)
    part_time_jobs = Job.objects.filter(job_type='Part Time',is_deleted=False)
    internship_jobs = Job.objects.filter(job_type='Internship',is_deleted=False)
    contract_jobs = Job.objects.filter(job_type='Contract',is_deleted=False)
    context = {
        'jobs': jobs,
        'filtered_jobs': filtered_jobs,
        'full_time_jobs': full_time_jobs,
        'part_time_jobs': part_time_jobs,
        'internship_jobs': internship_jobs,
        'contract_jobs':contract_jobs
    }
    return render(request,"job_portal/job-list.html",context=context)


def portfolios_home(request):
    portfolios = Portfolio.objects.filter(is_deleted=False)
    paginator = Paginator(portfolios,1000000000000)
    page_number = request.GET.get('page')
    portfolios = paginator.get_page(page_number)
    context = {
        'portfolios': portfolios,
        "title": 'Portfolio' 
    }
    return render(request, 'job_portal/portfolio.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            if not Portfolio.objects.filter(title=title,is_deleted=False).exists():
                Portfolio(                    
                    title = title,
                    description = description,
                    image = image
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Portfolio created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:portfolios')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Portfolio already exists",                        
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
        form = PortfolioForm()

        context = {
            "title": "Create Portfolio",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'sevendyne_admin/portfolio/create_portfolio.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def portfolios(request):
    portfolios = Portfolio.objects.filter(is_deleted=False)
    paginator = Paginator(portfolios,1000000000000)
    page_number = request.GET.get('page')
    portfolios = paginator.get_page(page_number)
    context = {
        'portfolios': portfolios,
        "title": 'Portfolio' 
    }
    return render(request, 'sevendyne_admin/portfolio/portfolios.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_portfolio(request, pk):
    instance = get_object_or_404(Portfolio.objects.filter(pk=pk, is_deleted=False))    
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Portfolio updated successfully.",                
                "redirect_url": reverse('main:portfolios')
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
        form = PortfolioForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Portfolio :" + instance.title,            
            "redirect": "true",
            "url": reverse('main:portfolios')
        }
        return render(request, 'sevendyne_admin/portfolio/create_portfolio.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def portfolio(request, pk):
    instance = get_object_or_404(Portfolio.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Portfolio'
    }
    return render(request, "sevendyne_admin/portfolio/portfolio.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_portfolio(request,pk):
    instance = get_object_or_404(Portfolio.objects.filter(pk=pk,is_deleted=False))    
    Portfolio.objects.filter(pk=pk).update(is_deleted=True,title=instance.title + "_deleted")
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Portfolio Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('main:portfolios')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json') 


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def hrms_dashboard(request):
    company=get_current_company(request)
    company_name = company.name
    employees = Employee.objects.filter(company=company,is_deleted=False)
    employees_count = Employee.objects.filter(company=company,is_deleted=False).count()
    clients = Client.objects.filter(company=company,is_deleted=False)[:5]
    clients_count =clients.count()
    current_date = datetime.date.today()
    jobs = Job.objects.filter(company=company,is_deleted=False)
    jobs_count =jobs.count()
    candidates = Candidate.objects.filter(is_deleted=False,is_blocked=False)
    candidates_count =candidates.count()
    absent_employees = AttendanceRegister.objects.filter(company=company,date=current_date, status='absent')[:4]
    absent_employees_count = absent_employees.count()
    try:
        hrms_client = get_object_or_404(HrmsClient, user=request.user, is_deleted=False)
        context = {
            'hrms_client': hrms_client,
            'company': company,
            'company_name':company_name,
            'employees_count': employees_count,
            'clients_count':clients_count,
            'candidates_count':candidates_count,
            'jobs_count':jobs_count,
            'clients':clients,
            'candidates':candidates,
            'employees':employees,
            'absent_employees': absent_employees,
            'absent_employees_count': absent_employees_count
        }    
        return render(request, "dashboard/admin-dashboard.html", context=context)
    except HrmsClient.DoesNotExist:
        return HttpResponse("HrmsClient not found for the user.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    
@login_required
@user_passes_test(has_employee_dashboard_permission, redirect_field_name=None)
def employee_dashboard(request):
    try:
        employee = get_object_or_404(Employee, user=request.user, is_deleted=False)
        company=employee.company
        approved_leave = Leave.objects.filter(employee=employee,company=company,is_approved=True,is_deleted=False).count()
        # total_leave = Leave.objects.filter(company=company,is_deleted=False).count()
         # Get the total leave days across all leave types
        total_leave = LeaveType.objects.filter(company=company, is_deleted=False).aggregate(total_leave=Sum('days'))['total_leave']
        # If total_leave is None (no leave records found), set it to 0
        total_leave = total_leave or 0
        remaining_leave = total_leave - approved_leave
        # Get upcoming holidays
        today = datetime.date.today()
        upcoming_holidays = Holiday.objects.filter(company=company, date__gte=today).order_by('date')

        context = {
            'company':company,
            'employee': employee,
            'approved_leave':approved_leave,
            'remaining_leave':remaining_leave,
            'upcoming_holidays': upcoming_holidays
        }    
        return render(request, "dashboard/employee-dashboard.html", context=context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found for the user.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def admin_dashboard(request):
    total_hrms_clients = 0
    hrms_clients = HrmsClient.objects.filter(is_deleted=False)
    monthly_hrms_clients = (
        HrmsClient.objects
        .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'))
        .values('month', 'year')
        .annotate(count=Count('id'))
        .order_by('year', 'month')
    )
    monthly_hrms_clients = json.dumps(list(monthly_hrms_clients))
    total_hrms_clients = hrms_clients.count()
    candidates = Candidate.objects.filter(is_deleted=False,is_blocked=False)
    candidates_count =candidates.count()
    jobs = Job.objects.filter(is_deleted=False)
    jobs_count =jobs.count()

    # Calculate number of jobs posted by each company for graph
    company_jobs = Job.objects.filter(is_deleted=False).values('company__name').annotate(job_count=Count('id'))
    company_jobs_data = [{'company': job['company__name'], 'job_count': job['job_count']} for job in company_jobs]
    company_jobs_json = json.dumps(company_jobs_data)

    skill_counts = {}
    # Count the number of candidates associated with each skill
    for candidate in candidates:
        skills = candidate.skills.split(',')
        for skill in skills:
            skill = skill.strip()  # Remove leading and trailing whitespaces
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    # Prepare data to pass to the template
    skill_counts_json = json.dumps(skill_counts)

    context = {
        'total_hrms_clients': total_hrms_clients,
        'monthly_hrms_clients' : monthly_hrms_clients,
        'candidates_count':candidates_count,
        'jobs_count':jobs_count,
        'company_jobs': company_jobs_json,
        'skill_counts_json':skill_counts_json
    }
    return render(request, "sevendyne_admin/sevendyne_admin.html", context=context)

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            contact_person = form.cleaned_data['contact_person']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            mobile = form.cleaned_data['mobile']
            fax = form.cleaned_data['fax']
            website = form.cleaned_data['website']
            logo = form.cleaned_data['logo']
            auto_id = get_auto_id(Company)
            creator = request.user
            updator = request.user
            if not Company.objects.filter(name=name).exists():
                data = Company.objects.create(                    
                    name = name, 
                    contact_person = contact_person, 
                    address = address, 
                    country = country, 
                    state = state, 
                    city = city, 
                    postal_code = postal_code, 
                    email = email, 
                    phone = phone, 
                    mobile = mobile, 
                    fax = fax, 
                    website = website,
                    logo = logo,
                    auto_id =auto_id,
                    creator = creator,
                    updator = updator
                )
                data.save()
                current_company = data
                is_default= True
                if CompanyAccess.objects.filter(user=request.user).exists():
                    is_default = False
                group = Group.objects.get(name="hrms_clients")
                CompanyAccess.objects.create(
                    user=request.user,
                    company=current_company,
                    group=group,
                    is_accepted=True,
                    is_default=is_default
                )
                PayrollItem.objects.create(company=current_company,name="Basic Salary",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="DA",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="HRA",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="ESI",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="Basic Salary",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="Leave",category="Deductions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="PF",category="Deductions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="TDS",category="Deductions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                SalarySetting.objects.create(company=current_company,da=5,hra=5,pf_emp=5,pf_org=5,esi_emp=5,esi_org=5,tds=0, auto_id=get_auto_id(SalarySetting),a_id = get_a_id(SalarySetting,request),creator = request.user,updator = request.user)
                LeaveType.objects.create(company=current_company,name="Casual Leave",days=12, auto_id=get_auto_id(LeaveType),a_id = get_a_id(LeaveType,request),creator = request.user,updator = request.user)
                request.session["current_company"] = str(current_company.pk)
                request.session.save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Company created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:hrms_dashboard')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Company already exists",                        
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
        form = CompanyForm()
        context = {
            "title": "Create Company",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'settings/settings.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def companies(request):
    company=get_current_company(request)
    companies = Company.objects.filter(id=company.id,is_deleted=False)
    paginator = Paginator(companies,1000000000000)
    page_number = request.GET.get('page')
    companies = paginator.get_page(page_number)
    context = {
        'companies': companies,
        "title": 'Companies' 
    }
    return render(request, "settings/companies.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_company(request, pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk, is_deleted=False))
    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(name__icontains=query))
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Company updated successfully.",                
                "redirect_url": reverse('main:companies')
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
        form = CompanyForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Company :" + instance.name,            
            "redirect": "true",
            "url": reverse('main:edit_company', kwargs={'pk': instance.pk})
        }
        return render(request, 'settings/settings.html', context)
    

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def company(request, pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Company'
    }
    return render(request, "settings/company.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_email_setting(request):
    current_company = get_current_company(request)
    if request.method == 'POST':
        form = EmailSettingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            auto_id = get_auto_id(EmailSetting)
            a_id = get_a_id(EmailSetting,request)
            company = current_company
            creator = request.user
            updator = request.user
            if not EmailSetting.objects.filter(company=current_company,is_deleted=False).exists():
                EmailSetting(                    
                    email = email,
                    password = password,
                    auto_id = auto_id,
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Email Setting created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:email_settings')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Email Setting already exists",                        
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
        form = EmailSettingForm()
        context = {
            "title": "Create Email Setting",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'settings/email-settings.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def email_settings(request):
    current_company = get_current_company(request)
    email_settings = EmailSetting.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(email_settings,1000000000000)
    page_number = request.GET.get('page')
    email_settings = paginator.get_page(page_number)
    context = {
        'email_settings': email_settings,
        "title": 'Email Settings',
        "is_email_settings" : True
    }
    return render(request, "settings/email-settings.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_email_setting(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(EmailSetting.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = EmailSettingForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Email Setting updated successfully.",                
                "redirect_url": reverse('main:email_settings')
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
        form = EmailSettingForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit EmailSetting :" + instance.email,            
            "redirect": "true",
            "url": reverse('main:edit_email_setting', kwargs={'pk': instance.pk})
        }
        return render(request, 'settings/email-settings.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def email_setting(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(EmailSetting.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Email Setting'
    }
    return render(request, "settings/email-setting.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_email_setting(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(EmailSetting.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    EmailSetting.objects.filter(pk=pk).update(is_deleted=True,email=instance.email + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Email Setting Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('main:email_settings')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   


