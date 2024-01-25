from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from main.models import Company, CompanyAccess


def company_required(function):
    print("company required decorator get request")
    def wrap(request, *args, **kwargs):
        if not CompanyAccess.objects.filter(user=request.user,is_accepted=True).exists():
            print("not user in company access")
            return HttpResponseRedirect(reverse('main:create_company'))
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
