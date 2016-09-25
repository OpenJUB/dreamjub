import typing

from . import settings
from . import auth

import ldap3


def get_all_courses(username: str, password: str) -> typing.Optional[
        typing.List[dict]]:
    """
    Gets a (raw) list of all courses.

    Note: This method may take a long time to fetch all courses.
    """

    # authenticate and return None if it fails
    conn = auth.connect_and_bind(username, password)

    if conn is None:
        return None

    # make a paged search
    results = conn.extend.standard.paged_search(
        search_base='ou=groups,%s' % (settings.LDAP_BASE_DN),
        search_filter='(&(objectclass=group)' +
                      '(sAMAccountName=GS-CAMPUSNET-COURSE-*))',
        search_scope=ldap3.SUBTREE,
        attributes=ldap3.ALL_ATTRIBUTES,
        paged_size=settings.LDAP_PAGE_SIZE,
        generator=False
    )

    # unbind
    conn.unbind()

    # return a list of results
    return list(results)


def get_all_users(username: str, password: str) -> typing.Optional[
        typing.List[dict]]:
    """
    Gets a (raw) list of all users inside LDAP.

    Note: This method may take a long time to fetch all students.
    """

    # authenticate and return None if it fails
    conn = auth.connect_and_bind(username, password)

    if conn is None:
        return None

    # make a paged searchla
    results = conn.extend.standard.paged_search(
        search_base='ou=users,%s' % (settings.LDAP_BASE_DN),
        search_filter='(objectclass=person)',
        search_scope=ldap3.SUBTREE,
        attributes=ldap3.ALL_ATTRIBUTES,
        paged_size=settings.LDAP_PAGE_SIZE,
        generator=False
    )

    # unbind
    conn.unbind()

    # return a list of results
    return list(results)
