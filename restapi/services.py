__author__ = 'christoph'
from restapi.models import Hostname, AddressUpdate
from django.conf import settings

class DyndnsService(object):

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

    def update_host_addresses(self, host, ipv4, ipv6):
        address_update = AddressUpdate(ipv4=ipv4, ipv6=ipv6, hostname=host)
        address_update.save()

    def delete_host(self, host):
        host.delete()

    def find_hosts_by_key_fingerprint(self, key_fingerprint):
        return Hostname.objects.filter(keyFingerprint=key_fingerprint)
