from jacobsdata import queries
from jacobsdata.parsing.user_components import component

def parse_all_users(username, password):
    """
    Parses all users from LDAP. 
    """
    
    # get all the components
    components = component.all()
    
    # find out the fields we need
    fields = set()
    for c in components:
        fields.update(c.fields)
    
    # get all the students with the given fields
    users = queries.get_all_users(username, password, attributes = list(fields))
    
    if users == None:
        return None
    
    # parse all the users individually
    return list(map(lambda u:parse_user(u, components), users))

def parse_user(user, components):
    """
    Parses a single user from LDAP with the given components
    """
    
    # target user object
    u = {}
    
    # iterate through the components
    for c in components:
        u.update(c.parse(user))
    
    # return the user
    return u