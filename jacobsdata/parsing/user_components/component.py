import typing


class UserParsingComponent(object):
    """ Represents a single component of users that can be parsed. """

    fields = []  # list of raw ldap fields required

    def parse(self, user: dict) -> dict:
        """ Parses a user object using this component and returns
        an appropriate dict object. """

        raise NotImplementedError

    @staticmethod
    def get_attribute(user: dict, attribute: str,
                      fallback: typing.Optional[typing.Any] = None,
                      single: bool = True) -> typing.Any:
        """ Gets an attribute from an LDAP object representing a group. """

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

    @staticmethod
    def get_dn(user: dict) -> str:
        """ Gets the DN of a user. """

        return user['dn']


def available() -> typing.List[UserParsingComponent]:
    """ Gets a list of all available UserParsingComponents. """

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
