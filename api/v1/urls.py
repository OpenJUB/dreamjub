"""
API v1 URL Configuration
"""

from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'users/me', views.CurrentStudentView.as_view())
]

urlpatterns += router.urls
