from urllib import quote

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.sites.models import Site

from forms import InviteForm
from signup.views import render_with_context
from utils import addToQueryString
import strings

@login_required
def index(request):
    vars = {}

    if request.method == "POST":
        invite_form = InviteForm(request.POST, request.FILES)
        if invite_form.is_valid():
            invite_form.save(request.user)

            return HttpResponseRedirect(addToQueryString(reverse("inviteindex"),
                {'notice': strings.INVITE_NOTICE_SUCCESS}))
        else:
            vars['invite_form'] = invite_form
    else:
        vars['invite_form'] = InviteForm()
        
    vars['siteurl'] = quote("http://%s" % Site.objects.get_current().domain)
    
    return render_with_context(request, "invite/invite_page.html", vars)