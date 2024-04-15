from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from hrms.models import HrmsClient
from main.functions import generate_form_errors

from .forms import LoginForm  # Import the LoginForm from your forms file

# Create your views here.

def user_login(request):
    form = LoginForm()  # Create an instance of the LoginForm

    if request.method == 'POST':
        form = LoginForm(request.POST)  # Bind the form with the submitted data
        # print("login post request")
        if form.is_valid():
            # Get the cleaned data from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("username",username)
            print("password",password)
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            print("Authenticated User:", user)
            # print("User Group:", user.groups.all())
            # print("User Groups:", user.groups.all())
            

            if user is not None:                

                # Check if the user is a superuser
                if user.is_superuser:
                    # Add the user to the 'sevendyne_admin' group
                    sevendyne_admin = Group.objects.get(name='sevendyne_admin')
                    user.groups.add(sevendyne_admin)
                    user.save()

                # Check user groups and redirect accordingly
                if user.groups.filter(name='sevendyne_admin').exists():
                    print("user belongs to sevendyne_admin")
                    # Log in the user
                    login(request, user)
                    return redirect('main:admin_dashboard')  
                elif user.groups.filter(name='hrms_clients').exists():
                    print("user belongs to hrms_clients group ")
                    # Check if the associated HrmsClient is enabled
                    if hasattr(user, 'hrmsclient') and user.hrmsclient.is_enabled:
                        print("hrms client is enabled ")
                        # Log in the user
                        login(request, user)
                        return redirect('main:hrms_dashboard') 
                    else:
                        print("hrms client is not enabled ")
                        error_message = "Your account is not enabled. Please contact technical@sevendyne.com"
                        return render(request, "authentication/login.html", {"form": form, "error_message": error_message})
                elif user.groups.filter(name='employee_group').exists():
                    print("user belongs to employee group ")
                    # Log in the user
                    login(request, user)
                    return redirect('main:employee_dashboard')  
                else:
                    print("user not an admin,employee or hrms client")
                    return redirect('user:user_login')
            else:
                # Authentication failed, show an error message
                print("user is none - invalid credentials")
                error_message = "Invalid login credentials. Please try again."
                return render(request, "authentication/login.html", {"form": form, "error_message": error_message})

    # If the request method is not POST, render the login form
    print("get request/ any user group")
    return render(request, "authentication/login.html", {"form": form})

def register(request):
    if request.method == 'POST':       
        email = request.POST['email']        
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        hashed_password = make_password(password)

        if not HrmsClient.objects.filter(username=username,is_deleted=False).exists():
            user, created = User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'email': email, 'first_name': first_name, 'last_name': last_name})
            print("user",user)
            # if created:
            print("user is created")
            # Get or create the 'hrms_clients' group
            hrms_clients_group, created = Group.objects.get_or_create(name='hrms_clients')

            # Add the user to the 'hrms_clients' group
            user.groups.add(hrms_clients_group)
            print("added to hrms_clients group")

            # Save the user to update group membership
            user.save()
            
            hrms_client = HrmsClient.objects.create(  
                user = user,                  
                first_name = first_name,
                last_name = last_name,
                username = username,
                password = password,
                email = email                  
            )
            message = "Registration Successful! Sevendyne will send you the credentials via email for login after verification.Thank you!"
            return render(request, "authentication/register.html", {"message": message})
        else:
            message = "Username already exists."
        return render(request, "authentication/register.html", {"message": message})      
    else:   
        return render(request, "authentication/register.html")


@login_required
def user_logout(request):
    # print("user_logout request got")
    logout(request)
    # print("logout")
    return redirect('user:user_login')

