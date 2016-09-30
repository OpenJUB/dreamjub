Login App
=========

This app provides a simple login view, and a simple login form template.
It behaves just like the standard Django template and view.



Login View
----------

Renders a login form on any GET request. Takes a `next` URL parameter, just 
like the standard Django view. Also respect kwargs for `template_name`. 
On POST, the login view returns a JSON object with the login status:

    {
      'login': Boolean,
      'detail': String
    }

The `login-form` element then issues a redirect to the URL specified in 
`next`, if its `redirect` property is set.



Login Element
-------------

Polymer element. Display a login form. Attributes are:
* `login_url` - URL of the login view, defaults to `/login`
* `next` - URL to redirect to after successful login
* `redirect` - Boolean to disable / enable redirect
* `opened` - If set, opens on page load
