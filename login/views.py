import json
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib import auth as auth_helpers
from django.views.decorators import debug


@debug.sensitive_post_parameters()
def login(request, template_name='login/login.html'):
    if request.method == 'POST':
        response_data = {}

        username = request.POST['username']
        password = request.POST['password']
        user = auth_helpers.authenticate(username=username, password=password)
        if user is not None:
            auth_helpers.login(request, user)

            response_data['status'] = 'OK'
        else:
            # Return an 'invalid login' error message.
            response_data['status'] = 'ERROR'
            response_data['detail'] = 'Your username or password is invalid.'

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if request.method == 'GET':
        return auth_views.login(request, template_name=template_name)