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
            return HttpResponseNotAllowed('<h1>Method not allowed</h1>')

    if len(hosts) == 0:
        return HttpResponseNotFound('<h1>Hostname not found</h1>')
    host = hosts[0]
    if request.method == 'GET':
        return get_host(request, host)
    elif request.method == 'PUT':
        return update_host(request, host)
    elif request.method == 'DELETE':
        return delete_host(request, host)

    return HttpResponseNotAllowed('<h1>Method not allowed</h1>')

def create_new_host(request, hostname):
    payload = json.loads(request.body)
    message = payload['message']
    signature = payload['signature']
    publicKey = message['publicKey']
    import_result = gpg.import_keys(publicKey)
    fingerprint = import_result.fingerprints[0]
    valid = verify_message(message, signature)
    if valid:
        newHostname = Hostname(hostname=hostname,keyFingerprint=fingerprint)
        newHostname.save()
        return HttpResponse('', status=201)
    else:
        return HttpResponseForbidden('', status=403)

def get_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def update_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def delete_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def verify_message(message, signature):
    messageAsString = json.dumps(message,separators=(',', ':'))
    messageFile = tempfile.NamedTemporaryFile(delete=False)
    messageFile.write(messageAsString)
    messageFile.close()
    verifyResult = gpg.verify_file(StringIO.StringIO(signature),messageFile.name)
    os.remove(messageFile.name)
    return verifyResult.valid
