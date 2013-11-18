from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from restapi.models import Hostname, AddressUpdate

@csrf_exempt
def single_host(request, hostname):
    if request.method == 'POST':
        return create_new_host(request, hostname)
    try:
        host = Hostname.objects.get(hostname=hostname)
    except Hostname.DoesNotExist:
        return HttpResponseNotFound('<h1>Hostname not found</h1>')
    if request.method == 'GET':
        return get_host(request, host)
    elif request.method == 'PUT':
        return update_host(request, host)
    elif request.method == 'DELETE':
        return delete_host(request, host)

    return HttpResponseNotAllowed('<h1>Method not allowed</h1>')

def create_new_host(request, hostname):
    return HttpResponse('<h1>Page was found</h1>')

def get_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def update_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')

def delete_host(request, host):
    return HttpResponse('<h1>Page was found</h1>')
