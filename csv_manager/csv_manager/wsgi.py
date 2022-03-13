"""
WSGI config for csv_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_manager.settings')

application = get_wsgi_application()
users = User.objects.all()
if not users:
    User.objects.create_superuser(username="admin", email="admin@example.com", password="admin",
                                  is_active=True, is_staff=True)
