from django.contrib.auth.models import User

from ldap3 import Server, Connection

LDAP_SERVER = 'jacobs.jacobs-university.de'
LDAP_USER_GROUP = 'JACOBS'
LDAP_BASE_DN = 'ou=users,ou=campusnet,dc=jacobs,dc=jacobs-university,dc=de'

class LDAPBackend(object):
    """
    Authenticates username and password against Jacobs LDAP domain.
    """

    def authenticate(self, username=None, password=None):
        # TODO Actually make this authenticate against LDAP

        """
        Checks if a given user and password can connect to campusnet.
        """

        login_valid = False

        # empty user => return False
        if username == "":
            return None

        try:
            # create a server and a connection
            server = Server(LDAP_SERVER)
            conn = Connection(server, "%s\\%s" % (LDAP_USER_GROUP, username), password=password)

            # do the actual bind, then unbind
            s = conn.bind()
            conn.unbind()

            login_valid = True
        except Exception as e:
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
