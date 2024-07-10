import json
import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse

from asset.forms import AssetForm
from asset.models import Asset
from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company, has_hrms_permission, has_hrms_permission
from main.functions import generate_form_errors


# candidate crud starts here
@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def create_asset(request):
    current_company = get_current_company(request)
    if request.method == 'POST':
        form = AssetForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            purchase_date = form.cleaned_data['purchase_date']
            photo = form.cleaned_data['photo']
            purchase_price = form.cleaned_data['purchase_price']
            useful_life_years = form.cleaned_data['useful_life_years']
            salvage_value = form.cleaned_data['salvage_value']
            bill = form.cleaned_data['bill']
            auto_id = get_auto_id(Asset)
            a_id = get_a_id(Asset,request)
            creator = request.user
            updator = request.user
            Asset(
                company = current_company,                    
                name = name, 
                description = description,
                purchase_date = purchase_date, 
                photo = photo, 
                purchase_price = purchase_price,
                useful_life_years = useful_life_years, 
                salvage_value = salvage_value, 
                bill = bill,
                auto_id = auto_id,
                a_id = a_id,
                creator = creator,
                updator = updator
            ).save()
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Asset created successfully.",
                "redirect": "true",
                "redirect_url": reverse('asset:assets')
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
        form = AssetForm()
        context = {
            "title": "Create Asset",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'asset/assets.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def assets(request):
    current_company = get_current_company(request)
    instances = Asset.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'assets': instances,
        "title": 'Assets' 
    }
    return render(request, "asset/assets.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def edit_asset(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Asset.objects.filter(pk=pk,company=current_company, is_deleted=False))
    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(name__icontains=query))
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Asset updated successfully.",                
                "redirect_url": reverse('asset:assets')
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
        form = AssetForm(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Asset :" + instance.name,            
            "redirect": "true",
            "url": reverse('asset:asset', kwargs={'pk': instance.pk})
        }
        return render(request, 'asset/assets.html', context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def asset(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Asset.objects.filter(pk=pk,company=current_company,is_deleted=False))
    context = {
        'asset': instance,
        'title': 'Asset',
    }
    return render(request, "asset/asset.html", context)


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def delete_asset(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Asset.objects.filter(pk=pk,company=current_company,is_deleted=False))   
    
    Asset.objects.filter(pk=pk).update(is_deleted=True,name=instance.name + "_deleted_" )    
    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Asset Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('asset:assets')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
    