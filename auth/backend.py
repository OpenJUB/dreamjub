from django.contrib.auth.models import User

class LDAPBackend(object):
    """
    Authenticates username and password against Jacobs LDAP domain.
    """

    def authenticate(self, username=None, password=None):
        # TODO Actually make this authenticate against LDAP
        return None
        
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='get from settings.py')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
