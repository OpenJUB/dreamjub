from django.conf import urls
from django.views import generic as generic_views

urlpatterns = [
    urls.url(r'^$', generic_views.TemplateView.as_view(
        template_name="portal/home.html"))
]
