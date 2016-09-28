from django.contrib.auth.models import User

from jacobsdata import auth

class LDAPBackend(object):
    """
    Authenticates username and password against Jacobs LDAP domain.
    """

    def authenticate(self, username=None, password=None):
        """
        Checks if a given user and password can connect to campusnet.
        """
        
        try:
            login_valid = auth.authenticate(username, password)
        except:
            return None
        
        if not login_valid:
            return None

        if login_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='get from settings.py')
                user.set_unusable_password()
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
