from django.conf.urls import include, url


from oauth2_provider import urls as oauth_urls

urlpatterns = [
    url(r'^o/', include(oauth_urls, namespace='oauth2_provider')),
]
