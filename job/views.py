import datetime
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from employee.models import Department
from job.forms import JobForm
from job.models import JOBTYPE_CHOICES, STATUS_CHOICES, Job
from django.core.paginator import Paginator
from main.decorators import company_required
from django.contrib.auth.decorators import login_required,user_passes_test

from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_admin_dashboard_permission, has_hrms_permission

#  views here.
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_job(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data['job_title']
            department = form.cleaned_data['department']
            job_location = form.cleaned_data['job_location']
            no_of_vacancies = form.cleaned_data['no_of_vacancies']
            experience = form.cleaned_data['experience']
            age = form.cleaned_data['age']
            salary_from = form.cleaned_data['salary_from']
            salary_to = form.cleaned_data['salary_to']
            job_type = form.cleaned_data['job_type']
            status = form.cleaned_data['status']
            start_date = form.cleaned_data['start_date']
            expired_date = form.cleaned_data['expired_date']
            description = form.cleaned_data['description']
            
            auto_id = get_auto_id(Job)
            a_id = get_a_id(Job,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Job.objects.filter(job_title=job_title,department=department,company=company,is_deleted=False).exists():
                Job(                    
                    job_title = job_title,
                    department = department,
                    job_location = job_location,
                    no_of_vacancies = no_of_vacancies,
                    experience = experience,
                    age = age,
                    salary_from = salary_from,
                    salary_to = salary_to,
                    job_type = job_type,
                    status = status,
                    start_date = start_date,
                    expired_date = expired_date,
                    description = description,
                    auto_id = auto_id, 
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Job created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('job:jobs')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Job already exists",                        
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
        form = JobForm()
        context = {
            "title": "Create Job",
            "form": form,
            "redirect": "true",
            "create":True
        }
        
        return render(request, 'job/jobs.html', context)

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def jobs(request):
    current_company = get_current_company(request)
    jobs = Job.objects.filter(company=current_company,is_deleted=False)

    paginator = Paginator(jobs,1000000000000)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    departments = Department.objects.filter(company=current_company,is_deleted=False)
    
    context = {
        'jobs': jobs,
        "title": 'Jobs',
        'departments':departments,

        'status_choices': STATUS_CHOICES,
        'job_type_choices': JOBTYPE_CHOICES,
    }
    return render(request, "job/jobs.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_job(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = JobForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Job updated successfully.",                
                "redirect_url": reverse('job:jobs')
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
        form = JobForm(instance=instance)
       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Job :" + instance.job_title,
            
            "redirect": "true",
            "url": reverse('job:edit_job', kwargs={'pk': instance.pk}),

        }
        return render(request, 'job/jobs.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def job(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Job',

    }
    return render(request, "job/jobs.html", context)

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_job(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Job.objects.filter(pk=pk).update(is_deleted=True,job_title=instance.job_title + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Job Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('job:jobs')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')

# All Jobs is for sevendyne admin dashboard
@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def all_jobs(request):
    jobs = Job.objects.filter(is_deleted=False)
    paginator = Paginator(jobs,1000000000000)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    departments = Department.objects.filter(is_deleted=False)
    
    context = {
        'jobs': jobs,
        "title": 'Jobs',
        'departments':departments,

        'status_choices': STATUS_CHOICES,
        'job_type_choices': JOBTYPE_CHOICES,
    }
    return render(request, "sevendyne_admin/jobs/all-jobs.html", context)



@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def job_view(request,pk):
    instance = get_object_or_404(Job.objects.filter(pk=pk,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Job'
    }
    return render(request, "sevendyne_admin/jobs/job-view.html", context)
