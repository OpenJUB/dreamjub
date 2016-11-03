import typing

from . import settings

import ldap3


def authenticate(username: str, password: str) -> bool:
    """ Authenticates a user against LDAP and return if the username /
    password combination is valid.
    """

    c = connect_and_bind(username, password)

    if c is None:
        return False
    else:
        c.unbind()
        return True


def connect_and_bind(username: str, password: str) -> typing.Optional[
        ldap3.Connection]:
    """
    Authenticates a user against LDAP and returns a bound connection object
    or None.
    """

    # we do not allow empty usernames
    if username == "":
        return None

    try:
        # create a server and a connection
        server = ldap3.Server(settings.LDAP_SERVER)
        conn = ldap3.Connection(server, "%s\\%s" % (
            settings.LDAP_USER_GROUP, username), password=password)

        # do the actual bind, then unbind
        s = conn.bind()

        # if we did not bind, return nothing
        if not s:
            conn.unbind()
            return None

        return conn
    except Exception as e:
        return None
