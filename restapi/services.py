__author__ = 'christoph'
from restapi.models import Hostname, AddressUpdate
from django.template import Context, loader, Template
from django.conf import settings
import os
import datetime
import subprocess

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
        zone_name = self.zone_name(hostname)
        self.nsd.add_zone(zone_name)

    def update_host_addresses(self, host, ipv4, ipv6):
        last_update = AddressUpdate.objects.filter(hostname=host).order_by('-created')[:1]
        if len(last_update) == 0 or last_update[0].ipv4 != ipv4 or last_update[0].ipv6 != ipv6:
            address_update = AddressUpdate(ipv4=ipv4, ipv6=ipv6, hostname=host)
            address_update.save()
            today = datetime.datetime.utcnow().date()
            updates_today = AddressUpdate.objects.filter(created__gt=today)
            serial = today.strftime("%Y%m%d{0:02d}").format(len(updates_today))
            zone_name = self.zone_name(host.hostname)
            self.nsd.update_zone(zone_name, ipv4, ipv6, serial)

    def delete_host(self, host):
        host.delete()
        zone_name = self.zone_name(host.hostname)
        self.nsd.delete_zone(zone_name)

    def zone_name(self, hostname):
        return '{}.{}'.format(hostname, settings.ZONE_DOMAIN)

    def find_hosts_by_key_fingerprint(self, key_fingerprint):
        return Hostname.objects.filter(keyFingerprint=key_fingerprint)

class NsdService(object):

    def add_zone(self, zone_name):
        self.write_zone_file(zone_name, '', '', 0)
        self.nsd_control('addzone', zone_name, settings.ZONES_PATTERN)

    def update_zone(self, zone_name, ipv4, ipv6, serial):
        self.write_zone_file(zone_name, ipv4, ipv6, serial)
        self.nsd_control('reload', zone_name)

    def delete_zone(self, zone_name):
        self.nsd_control('delzone', zone_name)
        self.delete_zone_file(zone_name)

    def write_zone_file(self, zone_name, ipv4, ipv6, serial):
        result = loader.render_to_string(settings.ZONE_TEMPLATE, {'zonename':zone_name, 'ipv4':ipv4, 'ipv6': ipv6, 'serial':serial})
        file = open('{}{}{}.zone'.format(settings.ZONES_DIRECTORY, os.path.sep, zone_name), 'w+')
        file.write(result)
        file.close()

    def delete_zone_file(self, zone_name):
        zone_file = '{}{}{}.zone'.format(settings.ZONES_DIRECTORY, os.path.sep, zone_name)
        if os.path.isfile(zone_file):
            os.remove(zone_file)

    def nsd_control(self, *args):
        if settings.NSD_CONTROL_PATH:
            if settings.SUDO_NSD_CONTROL:
                cmd = ['/usr/bin/sudo', settings.NSD_CONTROL_PATH]
            else:
                cmd = [settings.NSD_CONTROL_PATH]
            for arg in args:
                cmd.append(arg)
            subprocess.call(cmd)
