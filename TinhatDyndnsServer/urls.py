from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TinhatDyndnsServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hosts/(?P<hostname>[a-z0-9]+)/$', 'restapi.views.single_host'),
    url(r'^admin/', include(admin.site.urls)),
)
