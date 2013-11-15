from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import authentication, permissions
from restapi.models import Hostname, AddressUpdate

# Create your views here.
class HostnameView(GenericAPIView, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """
    View to list all users in the system.
    """
    model = Hostname

