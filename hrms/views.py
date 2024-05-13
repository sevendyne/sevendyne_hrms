import json
import datetime

from django.urls import reverse,reverse
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from main.functions import generate_form_errors, has_admin_dashboard_permission
from hrms.forms import HrmsClientEditForm, HrmsClientForm
from hrms.models import HrmsClient


# hrms_client crud starts here
@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_hrms_client(request):    
    if request.method == 'POST':
        form = HrmsClientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  
            if not HrmsClient.objects.filter(username=username,is_deleted=False).exists():
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    user.groups.add(hrms_clients_group)
                    hashed_password = make_password(password)
                    user.save()
                hashed_password = make_password(password)
                user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'first_name': first_name, 'last_name': last_name})
                if created:
                    hrms_clients_group, created = Group.objects.get_or_create(name='hrms_clients')
                    user.groups.add(hrms_clients_group)
                    user.save()
                HrmsClient(  
                    user = user,                  
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    password = password,
                    email = email                  
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "HRMS Client created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('hrms:hrms_clients')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "HRMS Client already exists",
                    "message": "HRMS Client with this username and password already exists",                        
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
        form = HrmsClientForm()
        context = {
            "title": "Create HRMS Client",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'sevendyne_admin/hrms_clients/create_hrms_client.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def hrms_clients(request):    
    instances = HrmsClient.objects.filter(is_deleted=False)
    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))    
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'HRMS Clients'            
    }
    return render(request, "sevendyne_admin/hrms_clients/hrms_clients.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_hrms_client(request, pk):    
    instance = get_object_or_404(HrmsClient.objects.filter(pk=pk, is_deleted=False))   
    if request.method == "POST":
        form = HrmsClientEditForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            user = instance.user
            user.username = data.username
            user.email = data.email
            user.password = make_password(data.password) 
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.email = data.email
            user.save()
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "HrmsClient updated successfully.",                
                "redirect_url": reverse('hrms:hrms_clients')
            }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
                "message": str(message),
                "title": "Form validation error"  
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = HrmsClientEditForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit HrmsClient :" + instance.first_name,            
            "redirect": "true",
            "url": reverse('hrms:edit_hrms_client', kwargs={'pk': instance.pk})
        }
        return render(request, 'sevendyne_admin/hrms_clients/create_hrms_client.html', context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def hrms_client(request, pk):    
    instance = get_object_or_404(HrmsClient.objects.filter(pk=pk,is_deleted=False))
    context = {
        'instance': instance,
        'title': 'HrmsClient'
    }
    return render(request, "sevendyne_admin/hrms_clients/hrms_client.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_hrms_client(request,pk):    
    instance = get_object_or_404(HrmsClient.objects.filter(pk=pk,is_deleted=False))    
    HrmsClient.objects.filter(pk=pk).update(is_deleted=True,first_name=instance.first_name)
    user = instance.user
    user.is_active = False
    user.save()
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "HRMS Client Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('hrms:hrms_clients')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
    
