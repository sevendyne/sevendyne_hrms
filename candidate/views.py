import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from main.decorators import company_required
from django.db.models import Q
from candidate.models import Candidate
from main.decorators import company_required

from candidate.forms import CandidateForm
from main.functions import generate_form_errors, get_auto_id
from main.models import Company, State

from django.http import JsonResponse

from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.contrib.auth.decorators import login_required, user_passes_test
from main.decorators import company_required
from main.functions import generate_form_errors, has_admin_dashboard_permission, has_hrms_permission

from hrms.models import HrmsClient


# candidate crud starts here

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
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
            auto_id = get_auto_id(Candidate)
            creator = request.user
            updator = request.user

            if not Candidate.objects.filter(name=name).exists():
                Candidate(                    
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
                    auto_id =auto_id,
                    creator = creator,
                    updator = updator
                ).save()
                print("candidate details is saved in db")
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Candidate created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('candidate:candidates')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Candidate already exists",                        
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
        form = CandidateForm()

        context = {
            "title": "Create Company",
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
    return render(request, "candidate/candidates-list.html", context)


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
            "title": "Edit Candidate :" + instance.name,
            
            "redirect": "true",
            "url": reverse('candidate:candidatesidate', kwargs={'pk': instance.pk}),


        }
        return render(request, 'candidate/create_candidate.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def candidate(request, pk):
    instance = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Company',

    }
    return render(request, "candidate/candidate.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_candidate(request,pk):
    instance = get_object_or_404(Candidate.objects.filter(pk=pk,is_deleted=False))
    
    Candidate.objects.filter(pk=pk).update(is_deleted=True,slug=instance.slug + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Candidate Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('candidate:candidates')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

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
            is_deleted=True, slug=instance.slug + "_deleted_" + str(instance.auto_id))

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
