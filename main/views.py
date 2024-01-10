import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from main.decorators import company_required
from django.db.models import Q
from main.decorators import company_required

from main.forms import CompanyForm
from main.functions import generate_form_errors, get_auto_id
from main.models import Company, State

from django.http import JsonResponse

def get_states(request):
    country_id = request.GET.get('country_id')
    if country_id:
        states = State.objects.filter(country_id=country_id)
        state_list = [{'id': state.id, 'name': state.name} for state in states]
        return JsonResponse({'states': state_list})
    else:
        return JsonResponse({'states': []})

# @login_required
# @company_required
# def app(request):
#     return HttpResponseRedirect(reverse('main:create_company'))
    # return HttpResponseRedirect(reverse('dashboard'))


@company_required
def hrms_dashboard(request):
    return render(request, 'base/hrms_base.html')


@company_required
def sevendyne_dashboard(request):
    return render(request, 'base/sevendyne_base.html')


# company crud starts here
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
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
            auto_id = get_auto_id(Company)
            creator = request.user
            updator = request.user

            if not Company.objects.filter(name=name).exists():
                Company(                    
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

                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Company created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('main:companies')
                }
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Company already exists",                        
                }
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            response_data = {
                "stable": "true",
                "status": "false",
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


# @company_required
def companies(request):
    instances = Company.objects.filter(is_deleted=False)
    paginator = Paginator(instances,1000000000000)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)
    context = {
        'instances': instances,
        "title": 'Companies' 
    }
    return render(request, "settings/companies.html", context)



# @company_required
def edit_company(request, pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk, is_deleted=False))
    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(name__icontains=query))


    if request.method == "POST":
        form = CompanyForm(request.POST, instance=instance)

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
        return render(request, 'settings/create_company.html', context)


# @company_required
def company(request, pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Company',

    }
    return render(request, "settings/company.html", context)


# @company_required
def delete_company(request,pk):
    instance = get_object_or_404(Company.objects.filter(pk=pk,is_deleted=False))
    
    Company.objects.filter(pk=pk).update(is_deleted=True,slug=instance.slug + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Company Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('main:companies')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

# @company_required
def delete_selected_companies(request):
    pks = request.GET.get('pk')
    if pks:
        pks = pks[:-1]

        pks = pks.split(',')
        for pk in pks:
            instance = get_object_or_404(Company.objects.filter(pk=pk, is_deleted=False))
            
        Company.objects.filter(pk=pk).update(
            is_deleted=True, slug=instance.slug + "_deleted_" + str(instance.auto_id))

        response_data = {
            "status": "true",            
            "title": "Successfully Deleted",
            "message": "Selected Company Successfully Deleted.",  

            "redirect" : "true",          
            "redirect_url": reverse('main:companies')
        }
    else:
        response_data = {
            "status": "false",
            "title": "Nothing selected",
            "message": "Please select any company first.",
        }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
