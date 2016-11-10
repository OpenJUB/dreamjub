"""
API URL Configuration

Future API versions will be added here
"""
from django.conf import urls

from .v1 import urls as api_v1

urlpatterns = [
    urls.url(r'v1/', urls.include(api_v1)),
]
