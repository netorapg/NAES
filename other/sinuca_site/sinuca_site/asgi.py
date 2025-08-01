"""
ASGI config for sinuca_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinuca_site.settings')

from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinuca_site.settings')

from .routing import application
