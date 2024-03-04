from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from main.models import Company, CompanyAccess
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def company_required(function):
    # print("company required decorator get request")
    def wrap(request, *args, **kwargs):
        if not CompanyAccess.objects.filter(user=request.user,is_accepted=True).exists():
            # print("not user in company access")
            return HttpResponseRedirect(reverse('main:create_company'))
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

# def company_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated and request.user.groups.filter(name='hrms_clients').exists():
#             if not CompanyAccess.objects.filter(user=request.user, is_accepted=True).exists():
#                 return HttpResponseRedirect(reverse('main:create_company'))
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('user:user_login')  # or any other redirect you prefer
#     return _wrapped_view