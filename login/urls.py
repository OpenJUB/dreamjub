from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from oauth2_provider import urls as oauth_urls

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'login/login.html'}),
    url(r'^o/', include(oauth_urls, namespace='oauth2_provider')),
]
