class UserParsingComponent(object):
    fields = [] # list of raw ldap fields required
        
    def parse(self, user):
        raise NotImplementedError
    
    def getAttribute(self, user, attribute, fallback = None, single = True):
        try:
            attlist = user['attributes'][attribute]
        except KeyError:
            attlist = []
        if single:
            if len(attlist) > 0:
                return attlist[0]
            else:
                return fallback
        else:
            return attlist
    def getDN(self, user):
        return user['dn']

def all():
    """
    Gets a list of all available UserParsingComponent. 
    """
    
    from . import base, college, contact, country, name, status, role
    
    return [
        base.BaseComponent(), 
        college.CollegeComponent(),
        contact.ContactComponent(),
        country.CountryComponent(),
        name.NameComponent(),
        status.StatusComponent(),
        role.RoleComponent()
    ]