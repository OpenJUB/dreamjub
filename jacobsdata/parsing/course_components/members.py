import typing

from . import component


class MemberComponent(component.CourseParsingComponent):
    """ Parses the members of a course. """

    fields = ['member']

    def parse(self, course: dict, parsed_users: typing.List[dict]) \
            -> dict:

        # get all the course members (as parsed_user objects)
        members = self.get_attribute(course, 'member', single=False)
        memberlist = list(filter(lambda u: u is not None, map(
            lambda u: self.get_user_by_ldap(u, parsed_users), members)))

        # filter them into faculty and students
        # instructors = list(filter(lambda u: u["isFaculty"], memberlist))
        students = list(filter(lambda u: not u["isFaculty"], memberlist))

        # instructors_un = list(map(lambda u: u["username"], instructors))
        students_un = list(map(lambda u: u["username"], students))

        return {
            # 'instructors': instructors_un, # empty
            'students': students_un
        }

    @staticmethod
    def get_user_by_ldap(ldap_dn: str, parsed_users: typing.List[object]) \
            -> object:
        """ Gets an LDAP user by name. """
        for u in parsed_users:
            if u["ldap_dn"] == ldap_dn:
                return u

        print(
            "Warning: Course has unknown 'member' with LDAP DN %r" % (ldap_dn))
        return None
