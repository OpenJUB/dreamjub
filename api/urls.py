"""
API URL Configuration

Future API versions will be added here
"""
from django.conf.urls import include, url

from .v1 import urls as api_v1

urlpatterns = [
    url(r'v1/', include(api_v1)),
]
