from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from apps.main.models import Company, CompanyAccess
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def company_required(function):
    def wrap(request, *args, **kwargs):
        if not CompanyAccess.objects.filter(user=request.user,is_accepted=True).exists():
            return HttpResponseRedirect(reverse('main:create_company'))
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap