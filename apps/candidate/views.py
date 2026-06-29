import json
import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

from apps.candidate.models import Candidate, Intern
from apps.job.models import INTERVIEW_CHOICES, CandidateInterview, CandidateJob, JobApplicant
from apps.main.decorators import company_required
from apps.main.functions import generate_form_errors, get_current_company, has_admin_dashboard_permission, has_hrms_permission
from apps.main.functions import generate_form_errors, get_candidate_id
from apps.candidate.forms import CandidateForm, InternForm
from apps.user.tasks import send_hrms_signup_email_notification


# candidate crud starts here
@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            photo = form.cleaned_data['photo']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            education = form.cleaned_data['education']
            experience = form.cleaned_data['experience']
            skills = form.cleaned_data['skills']
            certifications = form.cleaned_data['certifications']
            projects = form.cleaned_data['projects']
            additional_information = form.cleaned_data['additional_information']
            linkedin_profile = form.cleaned_data['linkedin_profile']
            github_profile = form.cleaned_data['github_profile']
            resume = form.cleaned_data['resume']
            job_type = form.cleaned_data['job_type']

            candidateid = get_candidate_id(request)

            if not Candidate.objects.filter(email=email).exists():
                Candidate(                    
                    first_name = first_name, 
                    last_name = last_name,
                    email = email, 
                    photo = photo, 
                    phone_number = phone_number,
                    address = address, 
                    education = education, 
                    experience = experience, 
                    skills = skills, 
                    certifications = certifications, 
                    projects = projects, 
                    additional_information = additional_information, 
                    linkedin_profile = linkedin_profile, 
                    github_profile = github_profile,
                    resume = resume,
                    job_type = job_type,
                    candidateid = candidateid
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Candidate created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('candidate:candidates')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Candidate already exists",                        
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
        form = CandidateForm()

        context = {
            "title": "Create Candidate",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'sevendyne_admin/candidate/create_candidate.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidates(request):
    instances = Candidate.objects.filter(is_deleted=False)
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Companies' 
    }
    return render(request, "sevendyne_admin/candidate/candidates.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_candidate(request, pk):
    instance = get_object_or_404(Candidate.objects.filter(pk=pk, is_deleted=False))
    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(name__icontains=query))
    if request.method == "POST":
        form = CandidateForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Candidate updated successfully.",                
                "redirect_url": reverse('candidate:candidates')
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
        form = CandidateForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Candidate :" + instance.email,            
            "redirect": "true",
            "url": reverse('candidate:candidate', kwargs={'pk': instance.pk})
        }
        return render(request, 'sevendyne_admin/candidate/create_candidate.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate(request, pk):
    instance = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Candidate',
    }
    return render(request, "sevendyne_admin/candidate/candidate.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_candidate(request,pk):
    instance = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))   
    if (CandidateJob.objects.filter(candidate=instance)).exists():
        is_ok = False
    elif (CandidateInterview.objects.filter(candidate=instance)).exists():
        is_ok = False
    elif (JobApplicant.objects.filter(candidate=instance)).exists():
        is_ok = False
    else:
        is_ok = True
    if is_ok == True:
        Candidate.objects.filter(pk=pk).update(is_deleted=True,email=instance.email + "_deleted_" )    
        response_data = {
            "status" : "true",        
            "title" : "Successfully Deleted",
            "message" : "Candidate Successfully Deleted.", 
            "redirect" : "true",       
            "redirect_url" : reverse('candidate:candidates')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        response_data = {
            "status": "false",
            "stable": "true",
            "title": "Permission for delete denied",
            "message": "Same candidate exists in CandidateJob,CandidateInterview or JobApplicant"                        
        }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_selected_candidates(request):
    pks = request.GET.get('pk')
    if pks:
        pks = pks[:-1]
        pks = pks.split(',')
        for pk in pks:
            instance = get_object_or_404(Candidate.objects.filter(pk=pk, is_deleted=False))            
        Candidate.objects.filter(pk=pk).update(
            is_deleted=True, email=instance.email + "_deleted_" + str(instance.auto_id))
        response_data = {
            "status": "true",            
            "title": "Successfully Deleted",
            "message": "Selected Candidate Successfully Deleted.", 
            "redirect" : "true",          
            "redirect_url": reverse('candidate:candidates')
        }
    else:
        response_data = {
            "status": "false",
            "title": "Nothing selected",
            "message": "Please select any candidate first.",
        }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
@company_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def hrms_candidates(request):
    company = get_current_company(request)
    instances = Candidate.objects.filter(is_deleted=False,is_blocked=False)    
    skills_query = request.GET.get("skills")
    if skills_query:
        instances = instances.filter(Q(skills__icontains=skills_query))    
    experience_query = request.GET.get("experience")
    if experience_query:
        instances = instances.filter(experience__gte=experience_query)        
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)

    # Fetch interview statuses for all candidates
    interview_statuses = {
        interview.candidate.id: interview.interview_status 
        for interview in CandidateInterview.objects.all()
    }

    # Fetch job statuses for all candidates
    candidate_job_statuses = {
        candidate_job.candidate.id: candidate_job.status 
        for candidate_job in CandidateJob.objects.filter(company=company,is_deleted=False)
    }

    # Create a list of candidates with their job statuses
    candidate_data = []
    for instance in instances:
        candidate_data.append({
            'instance': instance,
            'job_status': candidate_job_statuses.get(instance.id, None)
        })
    context = {
        'instances': instances,
        'candidate_data': candidate_data,
        'interview_statuses': interview_statuses, 
        "interview_choices": INTERVIEW_CHOICES,
        "title": 'Candidates' 
    }
    return render(request, "candidate/candidates.html", context)


def candidate_application(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            photo = form.cleaned_data['photo']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            education = form.cleaned_data['education']
            experience = form.cleaned_data['experience']
            skills = form.cleaned_data['skills']
            certifications = form.cleaned_data['certifications']
            projects = form.cleaned_data['projects']
            additional_information = form.cleaned_data['additional_information']
            linkedin_profile = form.cleaned_data['linkedin_profile']
            github_profile = form.cleaned_data['github_profile']
            resume = form.cleaned_data['resume']
            candidateid = get_candidate_id()
            if not Candidate.objects.filter(email=email).exists():
                candidate = Candidate.objects.create(                    
                    first_name = first_name, 
                    last_name = last_name,
                    email = email, 
                    photo = photo, 
                    phone_number = phone_number,
                    address = address, 
                    education = education, 
                    experience = experience, 
                    skills = skills, 
                    certifications = certifications, 
                    projects = projects, 
                    additional_information = additional_information, 
                    linkedin_profile = linkedin_profile, 
                    github_profile = github_profile,
                    resume = resume,
                    candidateid = candidateid
                )
                # Send email notification to sevendyne hr about candidate registration
                subject = 'Congratulations ! A Job Applicant, %s is registered in Sevendyne HRMS.' %str(first_name)
                enable_url = request.build_absolute_uri(reverse('candidate:candidate', kwargs={'pk': candidate.id}))
                html_message = render_to_string('candidate/email_templates/candidate_email_notification.html', {'candidate': candidate, 'enable_url': enable_url})
                plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = "sevendyne.technical@gmail.com"
                # Enqueue the email sending task
                send_hrms_signup_email_notification.delay(subject, plain_message, from_email, to_email, html_message)    
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Candidate created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:home')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Candidate already exists",                        
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
        form = CandidateForm()

        context = {
            "title": "Create Candidate",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'candidate/candidate_application.html', context)

        
def create_intern(request): 
    if request.method == 'POST':
        form = InternForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            intern_linkedin = form.cleaned_data['intern_linkedin']
            intern_git = form.cleaned_data['intern_git']
            resume = form.cleaned_data['resume']
            skills = form.cleaned_data['skills']
            domain = form.cleaned_data['domain']
            if not Intern.objects.filter(email=email,is_deleted=False).exists():                
                intern = Intern.objects.create( 
                    name = name,
                    email = email,
                    phone = phone,
                    intern_linkedin = intern_linkedin,
                    intern_git = intern_git,
                    resume = resume,
                    skills = skills,
                    domain = domain
                )  
                # Send email notification to sevendyne hr about intern registration
                subject = 'Congratulations ! An Intern, %s is registered in Sevendyne HRMS.' %str(name)
                enable_url = request.build_absolute_uri(reverse('candidate:intern', kwargs={'pk': intern.id}))
                html_message = render_to_string('candidate/email_templates/intern_email_notification.html', {'intern': intern, 'enable_url': enable_url})
                plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = "sevendyne.technical@gmail.com"
                # Enqueue the email sending task
                send_hrms_signup_email_notification.delay(subject, plain_message, from_email, to_email, html_message)                 
                response_data = {
                    "status": "true",
                    "title": "Successfully Enrolled",
                    "message": "Sevendyne will contact you for further procedure.",
                    "redirect": "true",
                    "redirect_url": reverse('main:job_portal')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "This email is already enrolled",                        
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
        form = InternForm()

        context = {
            "title": "Intern Enroll",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'internship/enrollment.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def interns(request):
    instances = Intern.objects.filter(is_deleted=False)
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Companies' 
    }
    return render(request, "sevendyne_admin/intern/interns.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def intern(request, pk):
    instance = get_object_or_404(Intern.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'Intern',
    }
    return render(request, "sevendyne_admin/intern/intern.html", context)

