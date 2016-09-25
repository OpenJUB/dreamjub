import typing

from jacobsdata import queries
from jacobsdata.parsing.course_components import component


def parse_all_courses(username: str, password: str,
                      parsed_users: typing.List[dict]):
    """ Parses all courses from LDAP. """

    # get all the components
    components = component.available()

    # find out the fields we need
    fields = set()
    for c in components:
        fields.update(c.fields)

    # get all the students with the given fields
    courses = queries.get_all_courses(username, password,
                                      attributes=list(fields))

    if courses is None:
        return None

    # parse all the users individually
    return list(
        map(lambda c: parse_course(c, parsed_users, components), courses))


def parse_course(course: dict, parsed_users: typing.List[dict],
                 components: typing.List[
                     component.CourseParsingComponent]) -> dict:
    """ Parses a single course from LDAP. """

    # target user object
    cd = {}

    # iterate through the components
    for c in components:
        cd.update(c.parse(course, parsed_users))

    # return the course
    return cd
