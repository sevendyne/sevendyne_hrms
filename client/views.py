import datetime
import json
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from client.forms import ClientForm
from client.models import Client
from main.decorators import company_required
from main.functions import generate_form_errors, get_a_id, get_auto_id, get_current_company
from django.urls import reverse


# Client Company crud starts here
@login_required
@company_required
def create_client(request):
    current_company = get_current_company(request)    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            company_name = form.cleaned_data['company_name']
            clientid = form.cleaned_data['clientid']
            auto_id = get_auto_id(Client)
            a_id = get_a_id(Client,request)
            company =current_company
            creator = request.user
            updator = request.user

            if not Client.objects.filter(company_name=company_name,company=company,is_deleted=False).exists():
                Client( 
                    firstname = firstname,
                    lastname = lastname,
                    email = email,
                    phone = phone,
                    address = address,
                    company_name = company_name,
                    clientid = clientid,
                    auto_id =auto_id,
                    a_id = a_id,
                    company = company,
                    creator = creator,
                    updator = updator
                ).save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Client created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('client:clients')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Already exists",
                    "message": "Client already exists",                        
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
        form = ClientForm()

        context = {
            "title": "Create Client",
            "form": form,
            "redirect": "true",
            "create":True
        }
        return render(request, 'client/clients.html', context)


@login_required
@company_required
def clients(request):
    current_company = get_current_company(request)
    clients = Client.objects.filter(company=current_company,is_deleted=False)
    paginator = Paginator(clients,1000000000000)
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)
    context = {
        'clients': clients,
        "title": 'Clients' 
    }
    return render(request, "client/clients.html", context)


@login_required
@company_required
def edit_client(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Client.objects.filter(pk=pk,company=current_company, is_deleted=False))    
    print("Client id",instance.pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()
            print("updated Client",data.company)

            response_data = {
                "status": "true",
                "redirect" : "true",
                "title": "Successfully Updated",
                "message": "Client updated successfully.",                
                "redirect_url": reverse('client:clients')
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
        form = ClientForm(instance=instance)

        context = {
            "form": form,
            "instance": instance,
            "title": "Edit Client :" + instance.company,
            
            "redirect": "true",
            "url": reverse('client:edit_client', kwargs={'pk': instance.pk}),

        }
        return render(request, 'client/clients.html', context)


@login_required
@company_required
def client(request, pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Client.objects.filter(pk=pk,company=current_company,is_deleted=False))

    context = {
        'instance': instance,
        'title': 'Client',

    }
    return render(request, "client/clientl", context)

@login_required
@company_required
def delete_client(request,pk):
    current_company = get_current_company(request)
    instance = get_object_or_404(Client.objects.filter(pk=pk,company=current_company,is_deleted=False))
    
    Client.objects.filter(pk=pk).update(is_deleted=True,company_name=instance.company_name + "_deleted_" + str(instance.auto_id))

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "Client Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('client:clients')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
   

