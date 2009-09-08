from django.contrib.flatpages.models import FlatPage

def navigation(context):
    context = {'pages': FlatPage.objects.all()}

    return context
