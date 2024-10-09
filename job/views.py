import datetime
import json

from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from job.tasks import send_hrms_credentials_email
from main.decorators import company_required
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required,user_passes_test
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_admin_dashboard_permission, has_hrms_permission
from job.forms import CandidateInterviewForm, CandidateInterviewStatusForm, CandidateJobForm, CandidateJobStatusForm, JobApplicantForm, JobApplicantStatusForm, JobForm
from job.models import INTERVIEW_CHOICES, JOBTYPE_CHOICES, STATUS_CHOICES, CandidateInterview, CandidateJob, Job, JobApplicant
from django.core.paginator import Paginator
from candidate.models import Candidate
from employee.models import Department
from django.http import HttpResponse
from sevendyne_hrms import settings


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_job(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = JobForm(request.POST, current_company=current_company)
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
            job_category = form.cleaned_data['job_category']
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
                    job_category = job_category,
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
        form = JobForm(current_company=current_company)
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
        'job_type_choices': JOBTYPE_CHOICES
    }
    return render(request, "job/jobs.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_job(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    if request.method == "POST":
        form = JobForm(request.POST, instance=instance, current_company=current_company)
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
        form = JobForm(instance=instance, current_company=current_company)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Job :" + instance.job_title,            
            "redirect": "true",
            "url": reverse('job:edit_job', kwargs={'pk': instance.pk})
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
        'title': 'Job'
    }
    return render(request, "job/jobs.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_job(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk,company=current_company,is_deleted=False))
    if (JobApplicant.objects.filter(job=instance)).exists():
        is_ok = False
    else:
        is_ok = True
    if is_ok == True:
        Job.objects.filter(pk=pk).update(is_deleted=True,job_title=instance.job_title + "_deleted_" + str(instance.auto_id))
        response_data = {
            "status" : "true",        
            "title" : "Successfully Deleted",
            "message" : "Job Successfully Deleted.", 
            "redirect" : "true",       
            "redirect_url" : reverse('job:jobs')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        response_data = {
            "status": "false",
            "stable": "true",
            "title": "Permission for delete denied",
            "message": "Same job exists in JobApplicant"                        
        }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


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
        'job_type_choices': JOBTYPE_CHOICES
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


#  candidate job views here.
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_candidate_job(request,pk):
    if not pk:
        raise ValueError("Candidate ID (pk) is required")    
    candidate = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))
    company = get_current_company(request)    
    if request.method == 'POST':
        form = CandidateJobForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data['job_title']
            job_location = form.cleaned_data['job_location']
            salary_from = form.cleaned_data['salary_from']
            salary_to = form.cleaned_data['salary_to']
            description = form.cleaned_data['description']
            status = "Job Offered"    
            if not CandidateJob.objects.filter(candidate=candidate,job_title=job_title,company=company,is_deleted=False).exists():
                instance = CandidateJob(  
                    candidate = candidate,                  
                    job_title = job_title,
                    job_location = job_location,
                    salary_from = salary_from,
                    salary_to = salary_to,
                    description = description,
                    status = status,
                    company =company
                )
                instance.save()

                 # Updating Candidate status to "Job Offered" only if the current company made the offer
                candidate.status = status
                candidate.save()                

                # Send email notification to sevendyne hrms admin
                subject = f'Job offered by {str(company)} to {str(candidate)}'
                action_url = request.build_absolute_uri(reverse('job:edit_candidate_job', kwargs={'pk': instance.pk}))
                html_message = render_to_string('job/email_templates/job_offered.html', {'instance': instance, 'action_url': action_url})
                plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = 'sevendyne.technical@gmail.com' 
                # Enqueue the email sending task
                send_hrms_credentials_email.delay(subject, plain_message, from_email, to_email, html_message)    
                
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Job offered successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('candidate:hrms_candidates')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Job already offered",                        
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
        form = CandidateJobForm()
        context = {
            "title": "Create Job Offer",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'candidate/candidates.html', context)
    

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate_jobs(request):
    jobs = CandidateJob.objects.filter(is_deleted=False)
    paginator = Paginator(jobs,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Candidate Job Offers'
    }
    return render(request, "sevendyne_admin/candidate/candidate-jobs.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_candidate_job(request, pk):
    instance = get_object_or_404(CandidateJob.objects.filter(pk=pk, is_deleted=False))    
    candidate = instance.candidate    
    if request.method == "POST":
        form = CandidateJobStatusForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            # Update candidate status
            candidate.status = data.status
            candidate.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Candidate Job Status updated successfully.",                
                "redirect_url": reverse('job:candidate_jobs')
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
        form = CandidateJobStatusForm(instance=instance)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Job :" + instance.job_title,
            
            "redirect": "true",
            "url": reverse('job:edit_candidate_job', kwargs={'pk': instance.pk})
        }
        return render(request, 'sevendyne_admin/candidate/edit_candidate_job.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate_job(request,pk):
    instance = get_object_or_404(CandidateJob.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Job'
    }
    return render(request, "sevendyne_admin/candidate/candidate-job.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_candidate_job(request,pk):
    instance = get_object_or_404(CandidateJob.objects.filter(pk=pk,is_deleted=False))    
    CandidateJob.objects.filter(pk=pk).update(is_deleted=True,job_title=instance.job_title + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Job Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('job:jobs')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


#  candidate interview views here.
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def create_candidate_interview(request,pk):
    candidate = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))
    current_company = get_current_company(request)   
    candidate_job = get_object_or_404(CandidateJob.objects.filter(candidate=candidate,company=current_company,is_deleted=False))     
    if request.method == 'POST':
        form = CandidateInterviewForm(request.POST)
        if form.is_valid():
            date_time = form.cleaned_data['date_time']
            additional_information = form.cleaned_data['additional_information']
            auto_id = get_auto_id(CandidateInterview)
            a_id = get_a_id(CandidateInterview,request)
            company =current_company
            creator = request.user
            updator = request.user
            if not CandidateInterview.objects.filter(candidate=candidate,date_time=date_time,company=company,is_deleted=False).exists():
                CandidateInterview(  
                    candidate = candidate,                  
                    date_time = date_time,
                    additional_information = additional_information,
                    auto_id = auto_id, 
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()
                status = "Interview Scheduled"
                candidate.status = status                
                candidate.save()
                candidate_job.status = status
                candidate_job.save()                
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Interview Scheduled successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('candidate:hrms_candidates')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Interview scheduled at same date and time",
                    "message": "Interview already scheduled",                        
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
        form = CandidateInterviewForm()
        context = {
            "title": "Schedule Job Interview",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'candidate/candidates.html', context)
    

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate_interviews(request):
    jobs = CandidateInterview.objects.filter(is_deleted=False)
    paginator = Paginator(jobs,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Candidate Job Interviews'
    }
    return render(request, "sevendyne_admin/candidate/candidate-interviews.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_candidate_interview(request, pk):
    instance = get_object_or_404(CandidateInterview.objects.filter(pk=pk, is_deleted=False))    
    if request.method == "POST":
        form = CandidateInterviewForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Candidate Interview updated successfully.",                
                "redirect_url": reverse('job:candidate_interviews')
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
        form = CandidateInterviewForm(instance=instance)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Interview :" + instance.candidate,
            
            "redirect": "true",
            "url": reverse('job:edit_candidate_interview', kwargs={'pk': instance.pk})
        }
        return render(request, 'sevendyne_admin/candidate/edit_candidate_interview.html', context)
    

@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def update_candidate_interview_status(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(CandidateInterview.objects.filter(company=current_company,candidate__id=pk, is_deleted=False))        
    if request.method == "POST":
        form = CandidateInterviewStatusForm(request.POST,instance=instance)
        data = form.save(commit=False)
        data.updator = request.user
        data.date_updated = datetime.datetime.now()
        data.save()        
        response_data = {
            "status": "true",
            "redirect" : "true",
            "title": "Successfully Updated",
            "message": "Candidate Interview Status updated successfully.",                
            "redirect_url": reverse('candidate:candidates')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = CandidateInterviewForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Interview Status:" ,
            
            "redirect": "true",
            "url": reverse('job:update_candidate_interview_status', kwargs={'pk': instance.pk}),

        }
        return render(request, 'candidate/candidates.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate_interview(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(CandidateInterview.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Job'
    }
    return render(request, "sevendyne_admin/candidate/candidate-interview.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_candidate_interview(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(CandidateInterview.objects.filter(pk=pk,company=current_company,is_deleted=False))    
    CandidateInterview.objects.filter(pk=pk).update(is_deleted=True,job_title=instance.job_title + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Interview Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('job:job_interviews')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


#  candidate job views here.
@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_job_applicant(request,pk):
    job = get_object_or_404(Job.objects.filter(pk=pk,is_deleted=False))
    company = job.company
    if request.method == 'POST':
        form = JobApplicantForm(request.POST, current_company=company)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']
            hiring_status = "Applicant"            
            auto_id = get_auto_id(Job)
            a_id = get_a_id(Job,request)
            creator = request.user
            updator = request.user
            if not JobApplicant.objects.filter(job=job,candidate=candidate,company=company,is_deleted=False).exists():
                JobApplicant(  
                    candidate = candidate,                  
                    job = job,
                    hiring_status = hiring_status,
                    auto_id = auto_id, 
                    a_id = a_id,
                    company =company,
                    creator = creator,
                    updator = updator
                ).save()   
                response_data = {
                    "status": "true",
                    "title": "Successfully Applied",
                    "message": "Job Applied successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('job:job_applicants')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Job Applicant already exists",                        
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
        form = JobApplicantForm(current_company=company)
        context = {
            "title": "Apply to Job",
            "form": form,
            "redirect": "true",
            "create":True
        }        
        return render(request, 'job/job-applicants.html', context)
    

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def job_applicants(request):
    jobs = JobApplicant.objects.filter(is_deleted=False)
    paginator = Paginator(jobs,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Job Applicants'
    }
    return render(request, "sevendyne_admin/candidate/job-applicants.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def edit_job_applicant_status(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Job.objects.filter(pk=pk, company=current_company,is_deleted=False))    
    if request.method == "POST":
        form = JobApplicantStatusForm(request.POST, instance=instance, current_company=current_company)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Job Applicant Status updated successfully.",                
                "redirect_url": reverse('job:job_applicants')
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
        form = JobApplicantStatusForm(instance=instance, current_company=current_company)       
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Job Applicant Status :" + instance.job_title,
            
            "redirect": "true",
            "url": reverse('job:edit_job_applicant', kwargs={'pk': instance.pk})
        }
        return render(request, 'job/jobs.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def job_applicant(request,pk):
    instance = get_object_or_404(JobApplicant.objects.filter(pk=pk,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Job Applicant'
    }
    return render(request, "sevendyne_admin/candidate/candidate-job.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
@company_required
def delete_job_applicant(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(JobApplicant.objects.filter(pk=pk,company=current_company,is_deleted=False))
    JobApplicant.objects.filter(pk=pk).update(is_deleted=True,job_title=instance.job_title + "_deleted_" + str(instance.auto_id))
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Job Applicant Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('job:job_applicants')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')

