from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

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
            # print("username",username)
            # print("password",password)
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            # print("Authenticated User:", user)
            # print("User Groups:", user.groups.all())
            # print("User Groups:", user.groups.all())
            

            if user is not None:
                # Log in the user
                login(request, user)

                # Check if the user is a superuser
                if user.is_superuser:
                    # Add the user to the 'sevendyne_admin' group
                    sevendyne_admin_group = Group.objects.get(name='sevendyne_admin')
                    user.groups.add(sevendyne_admin_group)
                    user.save()

                # Check user groups and redirect accordingly
                if user.groups.filter(name='sevendyne_admin').exists():
                    # print("sevendyne_admin")
                    return redirect('hrms:admin_dashboard')  
                elif user.groups.filter(name='hrms_clients').exists():
                    # print("user belongs to hrms_clients group ")
                    return redirect('hrms:home_hrms')  
                else:
                    # print("user not an admin or hrms client")
                    return redirect('user:user_login')
            else:
                # Authentication failed, show an error message
                print("user is none - invalid credentials")
                error_message = "Invalid login credentials. Please try again."
                return render(request, "authentication/login.html", {"form": form, "error_message": error_message})

    # If the request method is not POST, render the login form
    print("get request")
    return render(request, "authentication/login.html", {"form": form})


@login_required
def user_logout(request):
    # print("user_logout request got")
    logout(request)
    # print("logout")
    return redirect('user:user_login')

