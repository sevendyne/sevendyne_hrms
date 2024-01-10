from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from main.models import Company


def company_required(function):
    def wrap(request, *args, **kwargs):
        if not Company.objects.filter(user=request.user).exists():
            return HttpResponseRedirect(reverse('create_comapny'))
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

