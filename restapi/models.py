from django.db import models

# Create your models here.
class Hostname(models.Model):
    hostname = models.CharField(max_length=32)
    keyFingerprint = models.CharField(max_length=64)

class AddressUpdate(models.Model):
    hostname = models.ForeignKey(Hostname)
    ipv4 = models.CharField(max_length=15)
    ipv6 = models.CharField(max_length=45)
