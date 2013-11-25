from django.http import HttpResponse

__author__ = 'christoph'

class ErrorResponse(Exception):
    def __init__(self, status, content = ''):
        self.status = status
        self.content = content

class ErrorMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, ErrorResponse):
            return HttpResponse(exception.content, status=exception.status)
        return None
