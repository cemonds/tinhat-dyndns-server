from rest_framework.routers import SimpleRouter, Route

__author__ = 'christoph'

class RestAPIRouter(SimpleRouter):
    """
    A router which routes create request also directly to the detail url
    """
    routes = [
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'post': 'create',
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
    ]
