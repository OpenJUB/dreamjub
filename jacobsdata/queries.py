import typing

from . import settings
from . import auth

import ldap3


def query(username: str, password: str, search_base: str, filter: str) -> \
        typing.Optional[typing.List[dict]]:
    """
    Runs an arbitrary ldap filter and returns the list of results.
    """

    # authenticate and return None if it fails
    conn = auth.connect_and_bind(username, password)

    if conn is None:
        return None

    # make a paged search
    results = conn.extend.standard.paged_search(
        search_base='{},{}'.format(search_base, settings.LDAP_BASE_DN),
        search_filter=filter,
        search_scope=ldap3.SUBTREE,
        attributes=ldap3.ALL_ATTRIBUTES,
        paged_size=settings.LDAP_PAGE_SIZE,
        generator=False
    )

    # unbind
    conn.unbind()

    # return a list of results
    return list(results)


def get_all_courses(username: str, password: str) -> \
        typing.Optional[typing.List[dict]]:
    """
    Gets a (raw) list of all courses.

    Note: This method may take a long time to fetch all courses.
    """

    return query(username, password, 'ou=groups', '(&(objectclass=group)' +
                 '(sAMAccountName=GS-CAMPUSNET-COURSE-*))')


def get_all_users(username: str, password: str) -> \
        typing.Optional[typing.List[dict]]:
    """
    Gets a (raw) list of all users inside LDAP.

    Note: This method may take a long time to fetch all students.
    """

    return query(username, password, 'ou=users', '(objectclass=person)')
