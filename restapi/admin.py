from django.contrib import admin
from restapi.models import Hostname
from restapi.models import AddressUpdate

# Register your models here.
admin.site.register(Hostname)
admin.site.register(AddressUpdate)