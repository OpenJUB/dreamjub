from . import component

import re

email_pattern = re.compile(r'^(.*)@jacobs-university\.de$')


class BaseComponent(component.UserParsingComponent):
    """ Represents the basic fields of a user. """

    fields = ['employeeID', 'mail', 'sAMAccountName']

    def parse(self, user: dict) -> dict:
        # employeeID and ldap dn (internal identifiers)
        eid = int(self.get_attribute(user, 'employeeID'))
        ldap_dn = self.get_dn(user)

        active = ('OU=Active,' in ldap_dn)

        # email, we only use jacobs emails
        email = self.get_attribute(user, 'mail', '')
        if not email_pattern.match(email):
            if email != '':
                print("Warning: 'mail' is not a jacobs email: %r" % (email))
            email = ''

        # username
        username = self.get_attribute(user, 'sAMAccountName')

        return {
            'eid': eid,
            'ldap_dn': ldap_dn,
            'active': active,

            'username': username,
            'email': email
        }
