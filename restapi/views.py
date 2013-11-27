import os
from IPy import IP
import gnupg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import tempfile
import StringIO
from restapi.error import ErrorResponse
from restapi.services import DyndnsService
from django.conf import settings

gpg = gnupg.GPG(gpgbinary=settings.GPG_PATH,  gnupghome=settings.KEYS_DIRECTORY)
gpg.encoding = 'utf-8'

service = DyndnsService()

@csrf_exempt
def single_host(request, hostname):
    host = service.get_host(hostname)
    if request.method == 'POST':
        if host == None:
            return create_new_host(request, hostname)
        else:
            create_error('Not allowed', 405)

    if host == None:
        create_error('Not found', 404)
    if request.method == 'GET':
        return get_host(request, host)
    elif request.method == 'PUT':
        return update_host(request, host)
    elif request.method == 'DELETE':
        return delete_host(request, host)

    create_error('Not allowed', 405)

def create_new_host(request, hostname):
    payload = json.loads(request.body)
    try:
        message = payload['message']
        signature = payload['signature']
        publicKey = message['publicKey']
        import_result = gpg.import_keys(publicKey)
        if import_result.fingerprints:
            create_error('Invalid key', 422)
        fingerprint = import_result.fingerprints[0]
        valid = verify_message(message, signature, fingerprint)
        if valid:
            service.create_new_host(hostname, fingerprint)
            return HttpResponse('', status=201)
        else:
            create_error('Signature not valid for host key with fingerprint '+fingerprint, 403)
    except KeyError, e:
        create_error('Key '+e.message+' missing in request', 400)


def get_host(request, host):
    response = {}
    response['result'] = {'keyFingerprint':host.keyFingerprint,'created':host.created.isoformat()}
    response_string = json.dumps(response,separators=(',', ':'))
    return HttpResponse(response_string)

def update_host(request, host):
    payload = json.loads(request.body)
    try:
        message = payload['message']
        signature = payload['signature']
        ipv4 = check_ip_address_version(message['ipv4'], 4)
        if message['ipv6']:
            ipv6 = check_ip_address_version(message['ipv6'], 6)
        else:
            ipv6 = None
        fingerprint = host.keyFingerprint
        valid = verify_message(message, signature, fingerprint)
        if valid:
            service.update_host_addresses(host, ipv4, ipv6)
            return HttpResponse('', status=204)
        else:
            create_error('Signature not valid for host key with fingerprint '+host.keyFingerprint, 403)
    except KeyError, e:
        create_error('Key '+e.message+' missing in request', 400)

def check_ip_address_version(ip_string, version):
    try:
        ip = IP(ip_string)
        if ip.version() != version:
            create_error('Invalid version of ip address {}, expected version ipv{}'.format(ip_string, version), 422)
        return ip.strCompressed()
    except ValueError:
        create_error('Invalid ip address {}'.format(ip_string), 422)

def delete_host(request, host):
    payload = json.loads(request.body)
    try:
        message = payload['message']
        signature = payload['signature']
        confirm = message['confirm']
        if confirm != 'delete':
            create_error('Deletion of a hostname must be confirmed', 422)
        fingerprint = host.keyFingerprint
        valid = verify_message(message, signature, fingerprint)
        if valid:
            service.delete_host(host)
            other_hosts_with_same_key = service.find_hosts_by_key_fingerprint(fingerprint)
            if len(other_hosts_with_same_key) == 0:
                gpg.delete_keys(fingerprint)
            return HttpResponse('', status=204)
        else:
            create_error('Signature not valid for host key with fingerprint '+host.keyFingerprint, 403)
    except KeyError, e:
        create_error('Key '+e.message+' missing in request', 400)

def verify_message(message, signature, fingerprint):
    message_string = json.dumps(message,separators=(',', ':'))
    message_file = tempfile.NamedTemporaryFile(delete=False)
    message_file.write(message_string)
    message_file.close()
    verify_result = gpg.verify_file(StringIO.StringIO(signature),message_file.name)
    os.remove(message_file.name)
    return verify_result.valid and verify_result.fingerprint == fingerprint

def create_error(message, status):
    response = {}
    response['error'] = message
    response_string = json.dumps(response,separators=(',', ':'))
    raise ErrorResponse(status, response_string)
