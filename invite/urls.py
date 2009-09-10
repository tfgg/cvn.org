from django.conf.urls.defaults import *
import views

################################################################################
urlpatterns = patterns('invite.views',
    url(r'^$', views.index, name="inviteindex"),
)