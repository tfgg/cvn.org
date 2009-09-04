from django.conf.urls.defaults import *
import views

################################################################################
urlpatterns = patterns('casestudies',
    url(r'^$', views.home, name="home"),
    url(r'^user/(?P<id>[\w-]+)/$',
        views.user,
        name="user"),
    url(r'^logout/$',
        views.logout_view,
        name="logout"),
    url(r'^activate/(?P<key>\w+)/$',
        views.activate_user,
        name="activate"),
    url(r'^constituency/(?P<slug>[\w-]+)/$',
        views.constituency,
        name="constituency"),
    url(r'^constituency/(?P<slug>[\w-]+)/(?P<year>\d+)/$',
        views.constituency,
        name="constituency-by-year"),
    url(r'^add_constituency/$',
        views.add_constituency,
        name="add_constituency"),
    url(r'^delete_constituency/(?P<slug>[\w-]+)/$',
        views.delete_constituency,
        name="delete_constituency"),
)

