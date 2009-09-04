import types
import time

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.flatpages.models import FlatPage

from models import CustomUser, Constituency, RegistrationProfile
from forms import UserForm

from utils import addToQueryString
import settings

def render_with_context(request,
                        template,
                        context,
                        **kw):
    pages = FlatPage.objects.all()
    kw['context_instance'] = RequestContext(request)
    context['pages'] = pages
    return render_to_response(template,
                              context,
                              **kw)

def home(request):
    context = {}
    year = settings.CONSTITUENCY_YEAR
    constituencies = Constituency.objects.filter(year=year)
    count = CustomUser.objects\
            .aggregate(Count('constituencies',
                             distinct=True)).values()[0]
    total = constituencies.count()
    
    context['volunteers'] = CustomUser.objects.count()
    context['total'] = total
    context['count'] = count
    context['percent_complete'] = int(float(count)/total)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            user = authenticate(username=profile.user.email)
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            context['form'] = form
    else:
        context['form'] = UserForm()
    return render_with_context(request,
                               'home.html',
                               context)

def delete_constituency(request, slug):
    c = Constituency.objects.get(slug=slug)
    request.user.constituencies.remove(c)
    request.user.save()
    return HttpResponseRedirect(reverse('add_constituency'))

def add_constituency(request):
    my_constituencies = request.user.current_constituencies.all()
    context = {'my_constituencies': my_constituencies}
    if request.method == "POST":
        if request.POST.has_key('search'):
            query = request.POST.get('q', '')
            context['q'] = query
            if query:
                c = Constituency.objects.all().filter(name__contains=query)
                c = c.exclude(pk__in=my_constituencies)
                context['constituencies'] = c
        elif request.POST.has_key('add') and request.POST.has_key('add_c'):
            add_c = request.POST.getlist('add_c')
            if type(add_c) != types.ListType:
                add_c = [add_c]
            constituencies = Constituency.objects.all().filter(slug__in=add_c)
            constituencies = constituencies.exclude(pk__in=my_constituencies)
            request.user.constituencies.add(*constituencies.all())
            request.user.save()
                                      
    return render_with_context(request,
                               'add_constituency.html',
                               context)

def activate_user(request, key):
    profile = RegistrationProfile.objects.activate_user(key)
    error = notice = ""
    if not profile:
        error = "Sorry, that key was invalid"
    else:
        notice = "Thanks, you've successfully confirmed your email"
        user = authenticate(username=profile.user.email)
        login(request, user)
    context = {'error': error,
               'notice': notice}
    
    return HttpResponseRedirect(addToQueryString("/", context))

def user(request, id):
    context = {}
    user = get_object_or_404(CustomUser, pk=id)
    if user == request.user:
        context['user'] = user
    return render_with_context(request,
                               'user.html',
                               context)

def constituency(request, slug, year=None):
    if year:
        year = "%s-01-01" % year
    else:
        year = settings.CONSTITUENCY_YEAR
    try:
        constituency = Constituency.objects.all()\
                       .filter(slug=slug, year=year).get()
    except Constituency.DoesNotExist:
        raise Http404
    context = {'constituency':constituency}
    return render_with_context(request,
                               'constituency.html',
                               context)
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
