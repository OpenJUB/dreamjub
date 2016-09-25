import typing

from jacobsdata.parsing import user, course


def parse_all(u: str, password: str) -> typing.Tuple[
        typing.List[dict], typing.List[dict]]:
    """ Parses users and courses from LDAP. """

    # parse all the users
    users = user.parse_all_users(u, password)
    if users is None:
        return (None, None)

    courses = course.parse_all_courses(u, password, users)

    if courses is None:
        return (None, None)

    return (users, courses)
