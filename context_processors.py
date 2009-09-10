from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

def navigation(context):
    context = {'pages': FlatPage.objects.all()}

    return context

def current_site(context):
    context = {'current_site': Site.objects.get_current() }
    
    return context
