__author__ = 'christoph'
from restapi.models import Hostname, AddressUpdate
from django.template import Context, loader, Template
from django.conf import settings
import os
import datetime

class DyndnsService(object):

    def __init__(self):
        self.nsd = NsdService()

    def get_host(self, hostname):
        hosts = Hostname.objects.filter(hostname=hostname)
        if len(hosts) == 0:
            return None
        elif len(hosts) == 1:
            return hosts[0]
        else:
            assert False, 'Multiple hosts with the same hostname {} found'.format(hostname)

    def create_new_host(self, hostname, key_fingerprint):
        new_host = Hostname(hostname=hostname,keyFingerprint=key_fingerprint)
        new_host.save()
        self.nsd.add_zone(hostname)

    def update_host_addresses(self, host, ipv4, ipv6):
        address_update = AddressUpdate(ipv4=ipv4, ipv6=ipv6, hostname=host)
        address_update.save()
        today = datetime.datetime.utcnow().date()
        updates_today = AddressUpdate.objects.filter(created__gt=today)
        serial = today.strftime("%Y%m%d{}").format(len(updates_today))
        self.nsd.update_zone(host.hostname, ipv4, ipv6, serial)

    def delete_host(self, host):
        host.delete()
        self.nsd.update_zone(host.hostname)

    def find_hosts_by_key_fingerprint(self, key_fingerprint):
        return Hostname.objects.filter(keyFingerprint=key_fingerprint)

class NsdService(object):
    def add_zone(self, hostname):
        self.nsd_control('addzone', hostname, settings.ZONES_PATTERN)

    def update_zone(self, hostname, ipv4, ipv6, serial):
        result = loader.render_to_string(settings.ZONE_TEMPLATE, {'hostname':hostname, 'ipv4':ipv4, 'ipv6': ipv6, 'serial':serial})
        file = open('{}{}{}.zone'.format(settings.ZONES_DIRECTORY, os.path.sep, hostname), 'w')
        file.write(result)
        file.close()
        self.nsd_control('reload', '{}.zone'.format(hostname))

    def delete_zone(self, hostname):
        self.nsd_control('delzone', hostname)

    def nsd_control(self, *args):
        pass