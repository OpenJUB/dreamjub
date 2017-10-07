import json
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib import auth as auth_helpers
from django.views.decorators import debug
from django.shortcuts import render
from django.core import mail
from django import conf

from django.contrib.auth import models as auth_models
from django.views.decorators.http import require_http_methods

from oauth2_provider import views as oauth_views
from sesame import utils as token_utils

from dreamjub.models import Student


@debug.sensitive_post_parameters()
@require_http_methods(["GET", "POST"])
def login(request, template_name='login/login.html'):
    # get method => render the login form
    if request.method == 'GET':
        return login_get(request, template_name=template_name)

    # post method => send a true / false
    else:
        return login_post(request)


def login_get(request, template_name='login/login.html'):
    """ Handles a GET request on the login form. """

    # try to read the next parameter, fall back to '/'
    try:
        next = request.GET['next']
    except KeyError:
        next = '/'

    # and render the form
    return render(request, template_name=template_name,
                  context={'next': next})


@debug.sensitive_post_parameters()
@debug.sensitive_variables('email', 'username', 'password')
def login_post(request):
    email = None
    username = None
    password = None

    try:
        email = request.POST['email']
    except KeyError:
        pass

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        pass

    # try email
    if email is not None:
        response_data = try_email_login(request, email)
    # try username / password login
    elif username is not None:
        response_data = try_user_login(request, username, password)

    # nothing was given
    else:
        response_data = {'login': False,
                         'message': 'No credentials provided. '}

    # return some JSON
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@debug.sensitive_post_parameters()
@debug.sensitive_variables('email')
def try_email_login(request, email):
    """ Sends a magic login link to allow the user to login via email """

    # read the 'next' parameter, if applicable
    try:
        next = request.POST['next']
    except KeyError:
        next = '/'

    # try to get the user with the given email
    try:
        user = auth_models.User.objects.get(email=email)

    # if that fails, try to create a new student with that email
    except auth_models.User.DoesNotExist:
        try:
            student = Student.objects.get(email=email)
            user = student.get_or_create_user()
        except Student.DoesNotExist:
            user = None

    # if the user is not None, write them an email
    if user is not None:

        link = 'https://' + request.META['HTTP_HOST']
        link += next
        link += '&' if '?' in next else '?'
        link += token_utils.get_query_string(user)[1:]

        # we need some content for the email
        email_content = """Hey {0},
    did you just try to log in?

    If yes, you may do so by clicking the following link:

    {1}

    If no, please just ignore this mail.



    DO NOT REPLY TO THIS MAIL.
    WE WILL NOT READ IT.
    """.format(user.first_name, link)

        mail.send_mail('dreamjub login link', email_content,
                       conf.settings.EMAIL_HOST_USER,
                       [user.email])

    return {'login': True}


@debug.sensitive_post_parameters()
@debug.sensitive_variables('user', 'username', 'password')
def try_user_login(request, username, password):
    """ Logs in a user with username and password """

    # authenticate with a helper function
    user = auth_helpers.authenticate(username=username, password=password)

    # if that worked, return the actual login
    if user is not None:
        auth_helpers.login(request, user)
        return {'login': True}

    # oops, we failed
    else:
        return {'login': False,
                'message': 'Invalid username / password combination. '}


class AuthorizationView(oauth_views.AuthorizationView):
    template_name = "login/authorize.html"
