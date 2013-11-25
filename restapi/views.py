import os
from django.http.response import HttpResponseForbidden
import gnupg
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import tempfile
import StringIO
from restapi.models import Hostname, AddressUpdate

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
gpg = gnupg.GPG(gpgbinary='"C:\\Program Files (x86)\\GNU\\GnuPG\\gpg.exe"',  gnupghome=os.path.join(PROJECT_PATH, 'keys'))
gpg.encoding = 'utf-8'

@csrf_exempt
def single_host(request, hostname):
    hosts = Hostname.objects.filter(hostname=hostname)
    if request.method == 'POST':
        if len(hosts) == 0:
            return create_new_host(request, hostname)
        else:
            return create_error('Not allowed', 405)

    if len(hosts) == 0:
        return create_error('Not found', 404)
    host = hosts[0]
    if request.method == 'GET':
        return get_host(request, host)
    elif request.method == 'PUT':
        return update_host(request, host)
    elif request.method == 'DELETE':
        return delete_host(request, host)

    return create_error('Not allowed', 405)

def create_new_host(request, hostname):
    payload = json.loads(request.body)
    message = payload['message']
    signature = payload['signature']
    publicKey = message['publicKey']
    import_result = gpg.import_keys(publicKey)
    if import_result.count == 0:
        return create_error('Invalid key', 422)
    fingerprint = import_result.fingerprints[0]
    valid = verify_message(message, signature, fingerprint)
    if valid:
        newHostname = Hostname(hostname=hostname,keyFingerprint=fingerprint)
        newHostname.save()
        return HttpResponse('', status=201)
    else:
        return create_error('Signature not valid for key with fingerprint '+fingerprint, 403)

def get_host(request, host):
    response = {}
    response['result'] = {'keyFingerprint':host.keyFingerprint,'created':host.created.isoformat()}
    response_string = json.dumps(response,separators=(',', ':'))
    return HttpResponse(response_string)

def update_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def delete_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

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
    return HttpResponse(response_string, status=status)
