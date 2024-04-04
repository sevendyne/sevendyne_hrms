import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from main.decorators import company_required
from django.db.models import Q
from candidate.models import Candidate
from client.models import Client
from employee.models import AttendanceRegister, Employee, Leave
from job.models import Job
from main.decorators import company_required
from django.db.models.functions import ExtractMonth, ExtractYear


from main.forms import CompanyForm
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_employee_dashboard_permission
from main.models import Company, CompanyAccess, State

from django.http import JsonResponse

from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.contrib.auth.decorators import login_required, user_passes_test
from main.decorators import company_required
from main.functions import generate_form_errors, has_admin_dashboard_permission, has_hrms_permission

from hrms.models import HrmsClient
from payroll.models import PayrollItem
# def get_states(request):
#     country_id = request.GET.get('country_id')
#     if country_id:
#         states = State.objects.filter(country_id=country_id)
#         state_list = [{'id': state.id, 'name': state.name} for state in states]
#         return JsonResponse({'states': state_list})
#     else:
#         return JsonResponse({'states': []})

# @login_required
# @company_required
# def app(request):
#     return HttpResponseRedirect(reverse('main:create_company'))
    # return HttpResponseRedirect(reverse('dashboard'))

def job_portal(request):
    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    location = request.GET.get('location')

    # Fetch distinct job categories and job locations from existing job objects
    job_categories = Job.objects.filter(is_deleted=False).values_list('job_category', flat=True).distinct()
    job_locations = Job.objects.filter(is_deleted=False).values_list('job_location', flat=True).distinct()

    # Start with a base filter that ensures is_deleted is False
    filter_conditions = Q(is_deleted=False)

    # Add keyword filter if keyword is present
    if keyword:
        filter_conditions &= Q(job_title__icontains=keyword) | Q(description__icontains=keyword)

    # Add category filter if category is present
    if category:
        filter_conditions &= Q(job_category__icontains=category)

    # Add location filter if location is present
    if location:
        filter_conditions &= Q(job_location__icontains=location)

    # Filter jobs based on combined filter conditions
    filtered_jobs = Job.objects.filter(filter_conditions)
    jobs = Job.objects.filter(is_deleted=False)
    full_time_jobs = Job.objects.filter(job_type='Full Time',is_deleted=False)
    part_time_jobs = Job.objects.filter(job_type='Part Time',is_deleted=False)
    internship_jobs = Job.objects.filter(job_type='Internship',is_deleted=False)
    contract_jobs = Job.objects.filter(job_type='Contract',is_deleted=False)
    # job_categories = Job.objects.filter(is_deleted=False).values('job_category')

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
    # Start with a base filter that ensures is_deleted is False
    filter_conditions = Q(is_deleted=False)

    # Add keyword filter if keyword is present
    if keyword:
        filter_conditions &= Q(job_title__icontains=keyword) | Q(description__icontains=keyword)

    # Add category filter if category is present
    if category:
        filter_conditions &= Q(job_category__icontains=category)

    # Add location filter if location is present
    if location:
        filter_conditions &= Q(job_location__icontains=location)

    # Filter jobs based on combined filter conditions
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


def about(request):
    return render(request, 'job_portal/about.html')

def terms_and_conditions(request):
    return render(request, 'job_portal/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'job_portal/privacy_policy.html')

def home_hrms(request):
    return render(request, "home/index.html")

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def hrms_dashboard(request):
    company=get_current_company(request)
    # print("company logo",company.logo)
    company_name = company.name
    employees_count = Employee.objects.filter(company=company,is_deleted=False).count()
    clients = Client.objects.filter(company=company,is_deleted=False)[:5]
    clients_count =clients.count()
    # Step 1: Get the current date
    current_date = datetime.date.today()
    jobs = Job.objects.filter(company=company,is_deleted=False)
    jobs_count =jobs.count()
    candidates = Candidate.objects.filter(is_deleted=False,is_blocked=False)
    candidates_count =candidates.count()
    # Step 2: Query the AttendanceRegister model for absent entries today
    absent_employees = AttendanceRegister.objects.filter(company=company,date=current_date, status='absent')[:4]

    # Step 3: Retrieve the employees associated with the absent entries
    absent_employees_count = absent_employees.count()

    # print("hrms home request got")
    # Debugging: Print the user to verify it's the correct user
    # print("User:", request.user)
    # hrms_clients = HrmsClient.objects.filter(is_deleted=False)
    # print("all hrms clients",hrms_clients)

    try:
        # Retrieve the HrmsClient object associated with the logged-in user
        hrms_client = get_object_or_404(HrmsClient, user=request.user, is_deleted=False)
        # print("hrms client")
        # print(hrms_client)

        context = {
            'hrms_client': hrms_client,
            'company': company,
            'company_name':company_name,
            'employees_count': employees_count,
            'clients_count':clients_count,
            'candidates_count':candidates_count,
            'jobs_count':jobs_count,
            'clients':clients,
            'absent_employees': absent_employees,
            'absent_employees_count': absent_employees_count

        }
    
        return render(request, "dashboard/admin-dashboard.html", context=context)
    except HrmsClient.DoesNotExist:
        # Debugging: Print a message if the HrmsClient object is not found
        # print("HrmsClient not found for the user.")
        return HttpResponse("HrmsClient not found for the user.")
    except Exception as e:
        # Debugging: Print any other exceptions that might occur
        # print("Exception:", e)
        return HttpResponse(f"An error occurred: {str(e)}")
    
@login_required
@user_passes_test(has_employee_dashboard_permission, redirect_field_name=None)
def employee_dashboard(request):
    try:
        # Retrieve the HrmsClient object associated with the logged-in user
        employee = get_object_or_404(Employee, user=request.user, is_deleted=False)
        print("employee")
        company=employee.company
        print(employee)
        approved_leave = Leave.objects.filter(employee=employee,company=company,is_approved=True,is_deleted=False).count()
        total_leave = Leave.objects.filter(employee=employee,company=company,is_deleted=False).count()
        remaining_leave = total_leave - approved_leave
        context = {
            'company':company,
            'employee': employee,
            'approved_leave':approved_leave,
            'remaining_leave':remaining_leave
        }
    
        return render(request, "dashboard/employee-dashboard.html", context=context)
    except Employee.DoesNotExist:
        # Debugging: Print a message if the Employee object is not found
        print("Employee not found for the user.")
        return HttpResponse("Employee not found for the user.")
    except Exception as e:
        # Debugging: Print any other exceptions that might occur
        print("Exception:", e)
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

    # Initialize a dictionary to store skill counts
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
# company crud starts here
def create_company(request):
    # Check if the user is an HrmsClient and has already created a company
    # if HrmsClient.objects.filter(user=request.user).exists() and Company.objects.filter(creator=request.user).exists():
    #     response_data = {
    #         "status": "false",
    #         "stable": "true",
    #         "title": "Cannot create another company",
    #         "message": "An HRMS client can create only one company.",
    #     }
    #     return HttpResponse(json.dumps(response_data), content_type='application/json')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            print("company valid")
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
                #create company access
                # group = Group.objects.get(name="hrms_clients")
                
                is_default= True
                if CompanyAccess.objects.filter(user=request.user).exists():
                    is_default = False
                # Check if CompanyAccess already exists for the user and current_company
                # if not CompanyAccess.objects.filter(user=request.user, company=current_company).exists():
                #     is_default = True
                group = Group.objects.get(name="hrms_clients")

                CompanyAccess.objects.create(
                    user=request.user,
                    company=current_company,
                    group=group,
                    is_accepted=True,
                    is_default=is_default
                )
                # company_access_instance = CompanyAccess(user=request.user, company=current_company, group=group, is_accepted=True, is_default=is_default)
                # company_access_instance.save()

                # Add print statements to check if user=request.user is saved in CompanyAccess
                # print(f"CompanyAccess saved - User: {company_access_instance.user}, Company: {company_access_instance.company}, Group: {company_access_instance.group}")
                PayrollItem.objects.create(company=current_company,name="Basic Salary",category="Additions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)
                PayrollItem.objects.create(company=current_company,name="Leave",category="Deductions", auto_id=get_auto_id(PayrollItem),a_id = get_a_id(PayrollItem,request),creator = request.user,updator = request.user)

                request.session["current_company"] = str(current_company.pk)
                request.session.save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Company created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:hrms_dashboard')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Company already exists",                        
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
            print("status", response_data["status"])
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = CompanyForm()
        print("company get request")
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
    companies = Company.objects.filter(is_deleted=False)
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
            "url": reverse('main:edit_company', kwargs={'pk': instance.pk}),


        }
        return render(request, 'settings/settings.html', context)

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def company(request, pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Company',

    }
    return render(request, "settings/company.html", context)

