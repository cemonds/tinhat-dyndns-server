from django.db import models

# Create your models here.
class Hostname(models.Model):
    hostname = models.CharField(max_length=32, unique=True)
    keyFingerprint = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

class AddressUpdate(models.Model):
    hostname = models.ForeignKey(Hostname)
    ipv4 = models.CharField(max_length=15)
    ipv6 = models.CharField(max_length=45,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
