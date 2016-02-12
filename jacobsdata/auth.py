from . import settings

from ldap3 import Server, Connection

def authenticate(username, password):
    """
    Authenticates a user against LDAP and return if the
    username / password combination is valid. 
    """
    
    c = connect_and_bind(username, password)
    
    if c == None:
        return False
    else:
        c.unbind()
        return True

def connect_and_bind(username, password):
    """
    Authenticates a user against LDAP and returns a bound connection object or None. 
    """
    # we do not allow empty usernames
    if username == "":
        return None

    try:
        # create a server and a connection
        server = Server(settings.LDAP_SERVER)
        conn = Connection(server, "%s\\%s" % (settings.LDAP_USER_GROUP, username), password=password)

        # do the actual bind, then unbind
        s = conn.bind()
        
        # if we did not bind, return nothing
        if not s:
            conn.unbind()
            return None
        
        return conn
    except Exception as e:
        return None