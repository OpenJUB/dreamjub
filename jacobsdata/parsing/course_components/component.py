class CourseParsingComponent(object):
    fields = [] # list of raw ldap fields required
        
    def parse(self, course, parsed_users):
        raise NotImplementedError
    
    def getAttribute(self, course, attribute, fallback = None, single = True):
        try:
            attlist = course['attributes'][attribute]
        except KeyError:
            attlist = []
        if single:
            if len(attlist) > 0:
                return attlist[0]
            else:
                return fallback
        else:
            return attlist
    def getDN(self, course):
        return course['dn']

def all():
    """
    Gets a list of all available CourseParsingComponent. 
    """
    
    from . import desc, members, active
    
    return [
        desc.DescriptionComponent(),
        members.MemberComponent(), 
        active.ActiveComponent()
    ]