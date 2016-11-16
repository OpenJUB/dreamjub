from django.conf.urls import include, url

from . import views
from oauth2_provider import views as oauth_views


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^o/', include([
        url(r'^authorize/$', views.AuthorizationView.as_view(),
            name="authorize"),
        url(r'^token/$', oauth_views.TokenView.as_view(), name="token"),
        url(r'^revoke_token/$', oauth_views.RevokeTokenView.as_view(),
            name="revoke-token"),
        ]))
]
