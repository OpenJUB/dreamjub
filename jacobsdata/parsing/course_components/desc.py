from . import component

import typing
import re

desc_pattern = re.compile(
    r'^Global security group representing members of course ' +
    r'([^\s]+) \((.*)\)$')


class DescriptionComponent(component.CourseParsingComponent):
    """ Parses the description of a course. """

    fields = ['description']

    def parse(self, course: dict, parsed_users: typing.List[dict]) \
            -> dict:
        cid = ''
        name = ''

        # get description and match it
        desc = self.get_attribute(course, 'description', '')
        m = desc_pattern.match(desc)

        # parse the parts from it
        if m:
            cid = m.group(1)
            name = m.group(2)
        else:
            print("Warning: unknown course 'description': %r" % (desc))

        # ldap dn (internal identifiers)
        ldap_dn = self.get_dn(course)

        return {
            'cid': cid,
            'ldap_dn': ldap_dn,
            'name': name
        }
