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
    urls.url(r'courses', views.CourseView.as_view({'get': 'list'})),
]

urlpatterns += router.urls
