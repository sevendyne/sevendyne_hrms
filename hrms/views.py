import datetime
import json

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse
from django.db.models import Q
from django.http.response import HttpResponse
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required, user_passes_test

from main.functions import generate_form_errors, has_admin_dashboard_permission, has_hrms_permission
from hrms.forms import HrmsClientForm
from hrms.models import HrmsClient


@login_required
@user_passes_test(has_hrms_permission, redirect_field_name=None)
def hrms_dashboard(request):
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
        }

        return render(request, "home/home_hrms.html", context=context)
    except HrmsClient.DoesNotExist:
        # Debugging: Print a message if the HrmsClient object is not found
        # print("HrmsClient not found for the user.")
        return HttpResponse("HrmsClient not found for the user.")
    except Exception as e:
        # Debugging: Print any other exceptions that might occur
        # print("Exception:", e)
        return HttpResponse(f"An error occurred: {str(e)}")
    # Retrieve the HrmsClient object associated with the logged-in user
    # hrms_client = get_object_or_404(HrmsClient, user=request.user, is_deleted=False)
    # print("hrms client")
    # print(hrms_client)
    # context = {
    #     'hrms_client': hrms_client,
    # }

    # return render(request, "home_hrms.html", context=context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def admin_dashboard(request):
    total_hrms_clients = 0
    hrms_clients = HrmsClient.objects.filter(is_deleted=False)
    monthly_hrms_clients = HrmsClient.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    total_hrms_clients = hrms_clients.count()

    context = {
        'total_hrms_clients': total_hrms_clients,
        'monthly_hrms_clients' : monthly_hrms_clients
    }
    return render(request, "sevendyne_admin/sevendyne_admin.html", context=context)


# hrms_client crud starts here


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def create_hrms_client(request):
    
    if request.method == 'POST':
        # print("post")
        form = HrmsClientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print("valid")
            if not HrmsClient.objects.filter(username=username,is_deleted=False).exists():
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    # print(f"User with username '{username}' already exists.")
                    user.groups.add(hrms_clients_group)
                    # print("added existing user to hrms_clients group")
                    # Hash the password
                    hashed_password = make_password(password)
                    # Save the user to update group membership
                    user.save()
                    # Hash the password
                hashed_password = make_password(password)
                # Try to get the user, create one if it doesn't exist
                user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'first_name': first_name, 'last_name': last_name})
                # print("user,created",user,created)
                if created:
                    # print("user is created")
                    # Get or create the 'hrms_clients' group
                    hrms_clients_group, created = Group.objects.get_or_create(name='hrms_clients')

                    # Add the user to the 'hrms_clients' group
                    user.groups.add(hrms_clients_group)
                    # print("added to hrms_clients group")

                    # Save the user to update group membership
                    user.save()

                

                    # Check if the user is in the 'hrms_clients' group
                    # if hrms_clients_group in user.groups.all():
                    #     print("User successfully added to the 'hrms_clients' group.")
                    # else:
                    #     print("Failed to add user to the 'hrms_clients' group.")

                HrmsClient(  
                    user = user,                  
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    password = password,
                    email = email                  
                ).save()
                print("hrms client is saved in db")
                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "HRMS Client created successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('hrms:hrms_clients')
                }
                print("Redirect URL:", response_data["redirect_url"])
            else:               
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "HRMS Client already exists",
                    "message": "HRMS Client with this username and password already exists",                        
                }
                print("status inside", response_data["status"])
            print("status outside", response_data["status"])
            
        else:
            print('not valid')
            message = generate_form_errors(form, formset=False)
            print("message",message)
            response_data = {
                "stable": "true",
                "status": "form_error",  # Change status to 'form_error'
                "title": "Form validation error",
                "message": str(message),               
            }
            print("status", response_data["status"])
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = HrmsClientForm()

        context = {
            "title": "Create HRMS Client",
            "form": form,
            "redirect": "true",
            "create":True,

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
        "title": 'HRMS Clients',
            
    }
    return render(request, "sevendyne_admin/hrms_clients/hrms_clients.html", context)


@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def edit_hrms_client(request, pk):
    
    instance = get_object_or_404(HrmsClient.objects.filter(pk=pk, is_deleted=False))
    

    if request.method == "POST":
        form = HrmsClientForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)

            # Update associated User instance
            user = instance.user
            user.username = data.username
            user.email = data.email
            user.password = make_password(data.password)  # Hash the new password
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.email = data.email
            user.save()
            print("username",user.username)
            print("password",user.password)
            print("first name",user.first_name)
            print("last name",user.last_name)
            print("email",user.email)

            # Update HrmsClient instance
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
        form = HrmsClientForm(instance=instance)

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

    response_data = {
        "status" : "true",        
        "title" : "Successfully Deleted",
        "message" : "HRMS Client Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('hrms:hrms_clients')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')
    

@login_required
@user_passes_test(has_admin_dashboard_permission, redirect_field_name=None)
def delete_selected_hrms_clients(request):
    
    pks = request.GET.get('pk')
    if pks:
        pks = pks[:-1]

        pks = pks.split(',')
        for pk in pks:
            instance = get_object_or_404(HrmsClient.objects.filter(pk=pk, is_deleted=False))
            
            HrmsClient.objects.filter(pk=pk).update(
                is_deleted=True, slug=instance.slug + "_deleted_" + str(instance.auto_id))

        response_data = {
            "status": "true",            
            "title": "Successfully Deleted",
            "message": "Selected HRMS Client Successfully Deleted.",  

            "redirect" : "true",          
            "redirect_url": reverse('hrms:hrms_clients')
        }
        
    else:
        response_data = {
            "status": "false",
            "title": "Nothing selected",
            "message": "Please select any HRMS Client first.",
        }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

