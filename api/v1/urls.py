"""
API v1 URL Configuration
"""

from django.conf import urls
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.StudentViewSet)

urlpatterns = [
    urls.url(r'users/me', views.CurrentStudentView.as_view()),
]

urlpatterns += router.urls
