from . import component

import re
email_pattern = re.compile(r'^(.*)@jacobs-university\.de$')

class BaseComponent(component.UserParsingComponent):
    fields = ['employeeID', 'mail', 'sAMAccountName']
    
    def parse(self, user):
        # employeeID and ldap dn (internal identifiers)
        eid = int(self.getAttribute(user, 'employeeID'))
        ldap_dn = self.getDN(user)
        
        # email, we only use jacobs emails
        email = self.getAttribute(user, 'mail', '')
        if not email_pattern.match(email):
            if email != '':
                print("Warning: 'mail' is not a jacobs email: %r" % (email))
            email = ''
        
        # username
        username = self.getAttribute(user, 'sAMAccountName')
        
        return {
            'eid': eid, 
            'ldap_dn': ldap_dn, 
            'username': username, 
            'email': email
        }