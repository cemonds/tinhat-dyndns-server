"""
WSGI config for TinhatDyndnsServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

package_path = os.path.dirname(__file__)
root = os.path.dirname(package_path)
sys.path.append(root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TinhatDyndnsServer.wsgisettings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
