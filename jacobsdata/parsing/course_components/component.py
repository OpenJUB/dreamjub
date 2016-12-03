import typing


class CourseParsingComponent(object):
    """ Represents a single component of courses that can be parsed. """

    fields = []  # list of raw ldap fields required

    def parse(self, course: dict, parsed_users: typing.List[dict]) -> dict:
        """ Parses a course object using this component and returns
        an appropriate dict object. """

        raise NotImplementedError

    @staticmethod
    def get_attribute(course: dict, attribute: str,
                      fallback: typing.Optional[typing.Any] = None,
                      single: bool = True) -> typing.Any:
        """ Gets an attribute from an LDAP object representing a group. """

        # read out the course attribute
        try:
            attlist = course['attributes'][attribute]
        except KeyError:
            attlist = []

        # make sure that we actually got a list and not a single value
        if isinstance(attlist, str):
            attlist = [attlist]

        # if we want a single value, extract it.
        if single:
            try:
                if len(attlist) > 0:
                    return attlist[0]
                else:
                    return fallback
            except TypeError:
                return attlist

        # else return the normal value
        else:
            return attlist

    def get_dn(self, course: dict) -> str:
        """ Gets the DN of a course. """

        return course['dn']


def available() -> typing.List[CourseParsingComponent]:
    """ Gets a list of all available CourseParsingComponents. """

    from . import desc, members, active

    return [
        desc.DescriptionComponent(),
        members.MemberComponent(),
        active.ActiveComponent()
    ]
