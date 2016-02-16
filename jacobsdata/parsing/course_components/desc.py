from . import component

import re
desc_pattern = re.compile(r'^Global security group representing members of course ([^\s]+) \((.*)\)$')

class DescriptionComponent(component.CourseParsingComponent):
    fields = ['description']
    
    def parse(self, course, parsed_users):
        
        cid = ''
        name = ''
        
        # get description and match it
        desc = self.getAttribute(course, 'description', '')
        m = desc_pattern.match(desc)
        
        # parse the parts from it
        if m:
            cid = m.group(1)
            name = m.group(2)
        else:
            print("Warning: unknown course 'description': %r" % (desc))
        
        # ldap dn (internal identifiers)
        ldap_dn = self.getDN(course)
        
        return {
            'cid': cid, 
            'ldap_dn': ldap_dn, 
            'name': name
        }