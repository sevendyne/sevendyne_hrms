from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from sevendyne_hrms import settings
from hrms.models import HrmsClient
from user.forms import LoginForm


def user_login(request):
    form = LoginForm() 
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:          
                # Check if the user is a superuser
                if user.is_superuser:
                    # Add the user to the 'sevendyne_admin' group
                    sevendyne_admin = Group.objects.get(name='sevendyne_admin')
                    user.groups.add(sevendyne_admin)
                    user.save()
                # Check user groups and redirect accordingly
                if user.groups.filter(name='sevendyne_admin').exists():
                    login(request, user)
                    return redirect('main:admin_dashboard')  
                elif user.groups.filter(name='hrms_clients').exists():
                    # Check if the associated HrmsClient is enabled
                    if hasattr(user, 'hrmsclient') and user.hrmsclient.is_enabled:
                        login(request, user)
                        return redirect('main:hrms_dashboard') 
                    else:
                        error_message = "Your account is not enabled. Please contact technical@sevendyne.com"
                        return render(request, "authentication/login.html", {"form": form, "error_message": error_message})
                elif user.groups.filter(name='employee_group').exists():
                    login(request, user)
                    return redirect('main:employee_dashboard')  
                else:
                    return redirect('user:user_login')
            else:
                # Authentication failed, show an error message
                error_message = "Invalid login credentials. Please try again."
                return render(request, "authentication/login.html", {"form": form, "error_message": error_message})
    return render(request, "authentication/login.html", {"form": form})


def register(request):
    if request.method == 'POST':       
        email = request.POST['email']        
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        hashed_password = make_password(password)

        if not HrmsClient.objects.filter(username=username).exists():
            user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'first_name': first_name, 'last_name': last_name})
            hrms_clients_group, created = Group.objects.get_or_create(name='hrms_clients')

            # Add the user to the 'hrms_clients' group
            user.groups.add(hrms_clients_group)
            user.save()
            
            hrms_client = HrmsClient.objects.create(  
                user = user,                  
                first_name = first_name,
                last_name = last_name,
                username = username,
                password = password,
                email = email                  
            )
            # Send email notification to sevendyne admin
            subject = 'Congratulations ! An Hrms Client, %s is signed up in Sevendyne HRMS. Please enable the account' %str(first_name)
            enable_url = request.build_absolute_uri(reverse('hrms:edit_hrms_client', kwargs={'pk': hrms_client.id}))
            html_message = render_to_string('sevendyne_admin/hrms_clients/email_templates/email_notification.html', {'hrms_client': hrms_client, 'enable_url': enable_url})
            plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = "hr@sevendyne.com"
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                    
            message = "Registration Successful! Sevendyne will send you the credentials via email for login after verification.Thank you!"
            return render(request, "authentication/register.html", {"message": message})
        else:
            message = "Username already exists/existed."
        return render(request, "authentication/register.html", {"message": message})      
    else:   
        return render(request, "authentication/register.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('user:user_login')

