from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import viewsets, routers

admin.autodiscover()

# ViewSets define the view behavior.
class HostnameView(viewsets.ModelViewSet):
    model = User



# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TinhatDyndnsServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
)
